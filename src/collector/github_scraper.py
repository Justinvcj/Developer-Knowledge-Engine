import os
import time
import uuid
import base64
import sqlite3
import logging
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

def collect_github_readmes(repo_list: list[str], db_path: str):
    """
    Fetches README files from a list of GitHub repositories and stores them in the DB.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
    else:
        logging.warning("GITHUB_TOKEN not found in environment variables. Rate limits will be severely restricted.")

    # Ensure DB directory exists if not already
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        for repo_full_name in repo_list:
            logging.info(f"Processing repository: {repo_full_name}")
            
            # API endpoint for README
            api_url = f"https://api.github.com/repos/{repo_full_name}/readme"
            html_url = f"https://github.com/{repo_full_name}"
            
            try:
                response = requests.get(api_url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # GitHub API returns base64 encoded content
                    if 'content' in data and data['encoding'] == 'base64':
                        base64_content = data['content']
                        try:
                            decoded_content = base64.b64decode(base64_content).decode('utf-8')
                        except Exception as decode_err:
                            logging.error(f"Failed to decode content for {repo_full_name}: {decode_err}")
                            continue
                        
                        # Prepare data for insertion
                        doc_id = str(uuid.uuid4())
                        source_type = 'github'
                        
                        try:
                            cursor.execute('''
                                INSERT INTO raw_documents (document_id, source_type, url, content, processed)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (doc_id, source_type, html_url, decoded_content, False))
                            
                            conn.commit()
                            logging.info(f"Successfully saved README for {repo_full_name}")
                            
                        except sqlite3.IntegrityError:
                            logging.info(f"Repo already exists in DB, skipping: {repo_full_name} ({html_url})")
                            
                    else:
                        logging.warning(f"Unexpected response format for {repo_full_name}")
                        
                elif response.status_code == 404:
                    logging.warning(f"README not found for repository: {repo_full_name}")
                elif response.status_code in [403, 429]:
                    logging.error(f"Rate limit exceeded (HTTP {response.status_code}).")
                    if 'X-RateLimit-Reset' in response.headers:
                        reset_time = int(response.headers['X-RateLimit-Reset'])
                        wait_time = max(0, reset_time - int(time.time()))
                        logging.error(f"Rate limit resets in {wait_time} seconds.")
                    break # Stop processing if rate limited to avoid spamming
                else:
                    logging.error(f"Failed to fetch {repo_full_name}: HTTP {response.status_code}")
                    logging.debug(response.text)
                    
            except requests.exceptions.RequestException as e:
                logging.error(f"Network error while fetching {repo_full_name}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error processing {repo_full_name}: {e}")
                
            # Respect API rate limits
            time.sleep(1)
            
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Example usage
    sample_repos = ["facebook/react", "pallets/flask", "tiangolo/fastapi"]
    # Path relative to src/collector/github_scraper.py
    database_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "dke_storage.db")
    
    collect_github_readmes(sample_repos, database_path)
