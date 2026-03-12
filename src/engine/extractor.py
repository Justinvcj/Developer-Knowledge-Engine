import os
import sqlite3
import logging
import uuid
from pathlib import Path
from typing import List, Literal
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Node(BaseModel):
    entity_name: str = Field(description="Name of the entity, must be completely lowercase")
    entity_type: Literal['language', 'framework', 'database', 'tool', 'concept'] = Field(description="Strictly chosen entity type")

class Edge(BaseModel):
    source_entity_name: str = Field(description="Name of the source entity (lowercase)")
    target_entity_name: str = Field(description="Name of the target entity (lowercase)")
    relationship_type: Literal['uses', 'depends_on', 'alternative_to', 'improves', 'integrates_with'] = Field(description="Strictly chosen relationship type")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")

class KnowledgeGraph(BaseModel):
    nodes: List[Node] = Field(description="List of extracted nodes")
    edges: List[Edge] = Field(description="List of extracted edges connecting the nodes")

def extract_knowledge(db_path: str):
    """
    Extracts entities and relationships from processed documents using OpenAI,
    and stores them as nodes and edges in the graph tables.
    """
    client = OpenAI() # Expects OPENAI_API_KEY in environment variables
    
    conn = None
    try:
        db_path = Path(db_path).resolve()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Add 'extracted' column to 'raw_documents' if it doesn't exist
        try:
            cursor.execute("ALTER TABLE raw_documents ADD COLUMN extracted BOOLEAN DEFAULT 0")
            logging.info("Added 'extracted' column to 'raw_documents' table.")
            conn.commit()
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e).lower():
                logging.warning(f"Error checking/adding 'extracted' column: {e}")
                
        # 2. Select up to 3 documents that are processed but not yet extracted
        cursor.execute("""
            SELECT document_id, cleaned_content 
            FROM raw_documents 
            WHERE processed = 1 AND (extracted = 0 OR extracted = False OR extracted IS NULL)
            LIMIT 3
        """)
        rows = cursor.fetchall()
        
        if not rows:
            logging.info("No documents pending extraction found in the database.")
            return

        for doc_id, cleaned_content in rows:
            try:
                # Truncate content to first 3000 chars to save tokens
                content_to_process = cleaned_content[:3000] if cleaned_content else ""
                
                if not content_to_process:
                    logging.warning(f"Document {doc_id} has no cleaned_content. Marking as extracted to skip future attempts.")
                    cursor.execute("UPDATE raw_documents SET extracted = 1 WHERE document_id = ?", (doc_id,))
                    conn.commit()
                    continue
                
                logging.info(f"Extracting knowledge from document {doc_id}...")
                
                # 3. Call OpenAI LLM expecting KnowledgeGraph pydantic structured output
                completion = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a specialized knowledge extraction engine. Given a programming-related text, extract entities and the relationships between them. Ensure that all the referenced entity_names in the edges are also defined in the nodes. Ensure all entity names are strictly formatted in lowercase."
                        },
                        {"role": "user", "content": content_to_process}
                    ],
                    response_format=KnowledgeGraph
                )
                
                result = completion.choices[0].message.parsed
                
                extracted_nodes = result.nodes
                extracted_edges = result.edges
                
                nodes_added = 0
                edges_added = 0
                
                # 4. Insert Nodes
                for node in extracted_nodes:
                    node_id = str(uuid.uuid4())
                    
                    # Ensure entity_name uniqueness and handle insertion (converting to lower to strictly enforce)
                    entity_name_lower = node.entity_name.lower()
                    try:
                        cursor.execute("""
                            INSERT OR IGNORE INTO graph_nodes (node_id, entity_name, entity_type)
                            VALUES (?, ?, ?)
                        """, (node_id, entity_name_lower, node.entity_type))
                        
                        if cursor.rowcount > 0:
                            nodes_added += 1
                    except sqlite3.Error as e:
                        logging.warning(f"Error inserting node {entity_name_lower}: {e}")
                
                # 5. Insert Edges
                for edge in extracted_edges:
                    source_name_lower = edge.source_entity_name.lower()
                    target_name_lower = edge.target_entity_name.lower()
                    
                    # Look up node_ids for source and target
                    cursor.execute("SELECT node_id FROM graph_nodes WHERE entity_name = ?", (source_name_lower,))
                    source_row = cursor.fetchone()
                    
                    cursor.execute("SELECT node_id FROM graph_nodes WHERE entity_name = ?", (target_name_lower,))
                    target_row = cursor.fetchone()
                    
                    if source_row and target_row:
                        source_id = source_row[0]
                        target_id = target_row[0]
                        edge_id = str(uuid.uuid4())
                        
                        try:
                            # Insert the edge referencing the source and target node_ids and doc_id
                            cursor.execute("""
                                INSERT INTO graph_edges (edge_id, source_node, target_node, relationship_type, confidence_score, source_doc_id)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (edge_id, source_id, target_id, edge.relationship_type, edge.confidence_score, doc_id))
                            edges_added += 1
                        except sqlite3.Error as e:
                            logging.warning(f"Error inserting edge between {source_id} and {target_id}: {e}")
                    else:
                        logging.debug(f"Skipping edge {source_name_lower} -> {target_name_lower} due to missing node(s) in database.")
                
                # 6. Mark document as extracted
                cursor.execute("""
                    UPDATE raw_documents 
                    SET extracted = 1 
                    WHERE document_id = ?
                """, (doc_id,))
                
                # Safely commit transaction for the current document
                conn.commit()
                logging.info(f"Successfully extracted {len(extracted_nodes)} nodes ({nodes_added} newly added) and {len(extracted_edges)} edges ({edges_added} inserted) from document {doc_id}.")
                
            except Exception as e:
                logging.error(f"Error extracting knowledge from document {doc_id}: {e}")
                # Log error and skip this document, moving to the next
                conn.rollback()
        
        logging.info("Knowledge extraction process complete.")

    except sqlite3.Error as e:
        logging.error(f"Database error during extraction setup: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "dke_storage.db")
    
    logging.info("Starting knowledge extraction...")
    extract_knowledge(db_path)
