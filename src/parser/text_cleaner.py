import os
import sqlite3
import logging
import markdown
from bs4 import BeautifulSoup
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_unparsed_documents(db_path: str):
    """
    Fetches unparsed documents, converts Markdown to text, and updates the database.
    """
    conn = None
    try:
        # Resolve absolute path to ensure DB connection is correct
        db_path = Path(db_path).resolve()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Dynamically add the cleaned_content column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE raw_documents ADD COLUMN cleaned_content TEXT")
            logging.info("Added 'cleaned_content' column to 'raw_documents' table.")
        except sqlite3.OperationalError as e:
            # Column likely already exists
            if "duplicate column name" in str(e).lower():
                pass
            else:
                logging.warning(f"Error checking/adding column: {e}")
                
        # 2. Select unparsed documents
        cursor.execute("SELECT document_id, content FROM raw_documents WHERE processed = 0 OR processed = False")
        rows = cursor.fetchall()
        
        if not rows:
            logging.info("No unparsed documents found in the database.")
            return

        documents_processed = 0
        
        # 3. Iterate and parse
        for doc_id, raw_content in rows:
            try:
                # Convert Markdown to HTML
                html_content = markdown.markdown(raw_content)
                
                # Parse HTML and extract human-readable text
                soup = BeautifulSoup(html_content, "html.parser")
                text_content = soup.get_text(separator=' ', strip=True)
                
                # Remove excessive whitespace
                cleaned_text = ' '.join(text_content.split())
                
                # 4. Update row in database
                cursor.execute("""
                    UPDATE raw_documents 
                    SET cleaned_content = ?, processed = 1 
                    WHERE document_id = ?
                """, (cleaned_text, doc_id))
                
                documents_processed += 1
                
            except Exception as parse_error:
                logging.error(f"Failed to process document {doc_id}: {parse_error}")
                # Continue processing other documents even if one fails
                continue
                
        # Commit transactions
        conn.commit()
        logging.info(f"Successfully cleaned and updated {documents_processed} documents.")
        
    except sqlite3.Error as e:
        logging.error(f"Database error during processing: {e}")
    finally:
        # Proper cleanup
        if conn:
            conn.close()

if __name__ == "__main__":
    # Path relative to src/parser/text_cleaner.py
    database_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "dke_storage.db")
    
    # Execute the parser
    logging.info("Starting text parsing process...")
    process_unparsed_documents(database_path)
    logging.info("Text parsing process complete.")
