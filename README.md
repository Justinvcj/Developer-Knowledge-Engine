# Developer Knowledge Engine
> Transforming fragmented developer knowledge into a structured, queryable graph.

## Project Overview
The Developer Knowledge Engine (DKE) solves the problem of fragmented developer knowledge scattered across disparate documentation, forums, codebases, and articles. It works by ingesting raw content from various sources, cleaning and parsing the text, using Large Language Models to extract key technical entities and their relationships, and constructing a localized, interconnected queryable Knowledge Graph.

## Architecture
**Data Pipeline Flow:**
* **Data Collector** → Gathers raw HTML/Markdown content from target developer resources.
* **Content Parser** → Cleans raw semantic content and strips out unstructured formatting.
* **LLM Entity Extractor** → Uses GPT models to identify precise technical concepts and their relationships.
* **Knowledge Graph** → Connects extracted concepts locally using NetworkX and SQLite.
* **Streamlit UI** → Provides an interactive interface to query, visualize, and explore the knowledge graph.

## Tech Stack
* **Language:** Python 3.11
* **Database:** SQLite
* **Graph Processing:** NetworkX
* **LLM Integration:** OpenAI API
* **Frontend:** Streamlit

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd dke_project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the Environment Variables:**
   Create a `.env` file in the project root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Initialize the Database:**
   The SQLite databases (`data/*.db`, `data/*.sqlite3`) will be automatically initialized when running the pipeline scripts. Ensure that the `data/` directory exists.

## Usage
To operate the Developer Knowledge Engine, run the data pipeline scripts sequentially:

1. **Collect Data:**
   ```bash
   # Example: python src/collector/scraper.py
   ```
2. **Parse Content:**
   ```bash
   # Example: python src/parser/text_cleaner.py
   ```
3. **Extract Entities & Relationships:**
   ```bash
   python src/engine/extractor.py
   ```

## Current Status / Roadmap
* ✅ **Phase 1-3 (Pipeline & Extraction):** Complete. The system successfully collects raw documents, cleans them, and extracts structured entities and relationships via the LLM API.
* 🚧 **Phase 4-5 (Graph Querying & UI):** In active development. The upcoming focus is finalizing the local knowledge graph structure using NetworkX and building out the Streamlit user interface for querying and visualization.
