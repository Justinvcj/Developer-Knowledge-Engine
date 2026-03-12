import os
import sqlite3
import logging
from src.collector.github_scraper import collect_github_readmes

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_scraper_pipeline():
    """
    Executes the scraper and prints out the results to verify ingestion.
    """
    # Seed list of high-quality repositories
    test_repos = ["pallets/flask", "encode/starlette", "tiangolo/fastapi"]
    
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "data", "dke_storage.db")
    
    logging.info("Starting pipeline execution...")
    
    # 1. Run the collection function
    collect_github_readmes(test_repos, db_path)
    
    logging.info("Pipeline execution finished. Verifying database entries...")
    
    # 2. Verify results
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query the database
        cursor.execute("SELECT url, content FROM raw_documents")
        rows = cursor.fetchall()
        
        print("\n" + "="*50)
        print("DATABASE VERIFICATION RESULTS")
        print("="*50)
        
        # Print URL and first 150 characters of content for each row
        for url, content in rows:
            # Clean up newlines for cleaner printing
            preview = content[:150].replace('\n', ' ')
            print(f"\nURL: {url}")
            print(f"Content Preview: {preview}...")
            
        # Print total row count
        cursor.execute("SELECT COUNT(*) FROM raw_documents")
        count = cursor.fetchone()[0]
        
        print("\n" + "="*50)
        print(f"Total rows in raw_documents table: {count}")
        print("="*50)
        
    except sqlite3.Error as e:
        logging.error(f"Database verification error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    test_scraper_pipeline()
