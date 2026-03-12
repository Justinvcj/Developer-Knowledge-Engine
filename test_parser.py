import sqlite3
from pathlib import Path
from src.parser.text_cleaner import process_unparsed_documents

def test_parser():
    # Construct the absolute path to the database
    base_dir = Path(__file__).parent
    db_path = base_dir / "data" / "dke_storage.db"
    
    print(f"Running process_unparsed_documents targeting {db_path}...")
    process_unparsed_documents(str(db_path))
    print("Processing complete.\n")
    
    print("Connecting to database to verify results...")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query for the first 3 processed rows
        cursor.execute("""
            SELECT url, content, cleaned_content 
            FROM raw_documents 
            WHERE processed = 1 OR processed = True
            LIMIT 3
        """)
        rows = cursor.fetchall()
        
        if not rows:
            print("No processed documents found.")
            return

        for i, (url, raw_content, cleaned_content) in enumerate(rows, 1):
            print(f"--- Document {i} ---")
            print(f"URL: {url}")
            
            # Safely handle potential None values and slice to 200 characters
            raw_str = str(raw_content) if raw_content is not None else ""
            clean_str = str(cleaned_content) if cleaned_content is not None else ""
            
            # Formatting preview strings
            raw_preview = raw_str[:200].replace('\n', ' ')
            clean_preview = clean_str[:200].replace('\n', ' ')
            
            if len(raw_str) > 200:
                raw_preview += "..."
            if len(clean_str) > 200:
                clean_preview += "..."
                
            print(f"RAW PREVIEW: {raw_preview}")
            print(f"CLEAN PREVIEW: {clean_preview}")
            print("-" * 50 + "\n")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    test_parser()
