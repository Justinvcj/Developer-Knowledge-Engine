<div align="center">
  <h1>🧠 Developer Knowledge Engine</h1>
  <p>An automated ETL pipeline and AI-driven knowledge graph builder that turns unstructured documentation into queryable relational data.</p>

  <!-- TECH STACK BADGES -->
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://openai.com/"><img src="https://img.shields.io/badge/OpenAI_LLMs-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI"></a>
  <a href="https://networkx.org/"><img src="https://img.shields.io/badge/NetworkX-000000?style=for-the-badge&logo=python&logoColor=white" alt="NetworkX"></a>
  <a href="https://www.sqlite.org/"><img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"></a>
  <a href="https://docs.github.com/en/rest"><img src="https://img.shields.io/badge/GitHub_API-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub API"></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"></a>
</div>

<br/>

## 📖 Overview
Developer Knowledge Engine solves the problem of fragmented documentation by actively scraping developer repositories and constructing an intelligent, interactive Knowledge Graph. By leveraging OpenAI Large Language Models (LLMs) and strict Pydantic schemas, the system extracts critical architectural entities and relationships, transforming raw text into an O(1) queryable structure.

## ✨ Key Features
- **🔄 Automated ETL Pipeline:** Extracts unstructured markdown files directly from remote GitHub repositories and standardizes them locally.
- **🤖 AI Entity Extraction:** Utilizes LLMs to read through documentation and intelligently extract technical terms, design patterns, and relational data.
- **🛡️ Strict Data Validation:** Ensures zero hallucinations in graph structure by forcing AI outputs through predefined Pydantic validation schemas.
- **🕸️ Relational Knowledge Graph:** Constructs an interconnected, interactive graph utilizing `NetworkX` and stores the persistent data locally via `SQLite`.
- **📊 Visual Interface:** Allows developers to seamlessly navigate complex relationships and search through the parsed knowledge base.

## 🏗️ Architecture Workflow
```text
[ GitHub Repository ] --> (Scraping via API) --> [ Raw Markdown ]
                                                        |
                                                        V
[ SQLite Storage ] <-- (Pydantic Validation) <-- [ OpenAI LLM Parsing ]
         |
         V
[ NetworkX Graph Builder ] --> [ Interactive Streamlit Frontend ]
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- OpenAI API Key
- GitHub Personal Access Token

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Justinvcj/Developer-Knowledge-Engine.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your environment variables in `.env`:
   ```env
   OPENAI_API_KEY=your_openai_key
   GITHUB_TOKEN=your_github_token
   ```
4. Run the ETL Pipeline:
   ```bash
   python pipeline.py
   ```
5. Launch the Visualizer:
   ```bash
   streamlit run app.py
   ```

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
