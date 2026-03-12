import sqlite3
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def init_database():
    # Construct path to the database (../data/dke_storage.db relative to src)
    db_path = Path(__file__).parent.parent / "data" / "dke_storage.db"
    
    # Ensure the data directory exists before connecting
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = None
    try:
        # Connect to SQLite (this will create the DB file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        
        # Enforce foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        
        # Table 1: raw_documents
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS raw_documents (
                document_id TEXT PRIMARY KEY,
                source_type TEXT,
                url TEXT UNIQUE,
                content TEXT,
                processed BOOLEAN DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table 2: graph_nodes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS graph_nodes (
                node_id TEXT PRIMARY KEY,
                entity_name TEXT UNIQUE,
                entity_type TEXT
            )
        ''')
        
        # Table 3: graph_edges
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS graph_edges (
                edge_id TEXT PRIMARY KEY,
                source_node TEXT,
                target_node TEXT,
                relationship_type TEXT,
                confidence_score REAL,
                source_doc_id TEXT,
                FOREIGN KEY (source_node) REFERENCES graph_nodes (node_id),
                FOREIGN KEY (target_node) REFERENCES graph_nodes (node_id),
                FOREIGN KEY (source_doc_id) REFERENCES raw_documents (document_id)
            )
        ''')
        
        conn.commit()
        logging.info(f"Database initialized successfully at {db_path.resolve()}")
        
    except sqlite3.Error as e:
        logging.error(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database()
