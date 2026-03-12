import os
import sqlite3
import logging
from src.engine.extractor import extract_knowledge
from dotenv import load_dotenv

load_dotenv()

# Configure logging to see the extractor's output clearly
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def verify_extraction(db_path: str):
    """
    Runs the extraction process and then queries the database 
    to verify nodes and edges were inserted correctly.
    """
    logging.info("--- Starting Knowledge Extraction ---")
    
    # 1. Run the extraction
    extract_knowledge(db_path)
    
    logging.info("--- Validating Database Integrity ---")
    
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 2. Node Verification
        cursor.execute("SELECT COUNT(*) FROM graph_nodes")
        total_nodes = cursor.fetchone()[0]
        print(f"\n[Verification] Total Nodes in DB: {total_nodes}")
        
        print("\n[Verification] Sample Nodes (Up to 10):")
        cursor.execute("SELECT entity_name, entity_type FROM graph_nodes LIMIT 10")
        sample_nodes = cursor.fetchall()
        for name, type_ in sample_nodes:
            print(f"Entity: {name} | Type: {type_}")
            
        # 3. Edge Verification
        cursor.execute("SELECT COUNT(*) FROM graph_edges")
        total_edges = cursor.fetchone()[0]
        print(f"\n[Verification] Total Edges in DB: {total_edges}")
        
        print("\n[Verification] Sample Edges (Up to 10):")
        
        # SQL JOIN query to resolve source_node and target_node UUIDs to entity_name
        query = """
        SELECT 
            sn.entity_name AS source_name,
            e.relationship_type,
            tn.entity_name AS target_name,
            e.confidence_score
        FROM 
            graph_edges e
        JOIN 
            graph_nodes sn ON e.source_node = sn.node_id
        JOIN 
            graph_nodes tn ON e.target_node = tn.node_id
        LIMIT 10
        """
        
        cursor.execute(query)
        sample_edges = cursor.fetchall()
        
        for source, rel_type, target, conf in sample_edges:
            print(f"{source} --> {rel_type} --> {target} (Confidence: {conf})")
            
    except sqlite3.Error as e:
        print(f"Database error during verification: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    database_path = os.path.join(os.path.dirname(__file__), "data", "dke_storage.db")
    verify_extraction(database_path)
