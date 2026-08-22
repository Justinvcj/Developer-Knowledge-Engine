<div align="center">

# Developer Knowledge Engine

**Automated documentation ETL pipeline and knowledge graph builder transforming unstructured markdown into structured, queryable graphs.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI_API-412991?logo=openai&logoColor=white)](https://openai.com)
[![NetworkX](https://img.shields.io/badge/NetworkX-Graph-000000?logo=python&logoColor=white)](https://networkx.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)

[Report Bug](https://github.com/Justinvcj/Developer-Knowledge-Engine/issues) Â· [Request Feature](https://github.com/Justinvcj/Developer-Knowledge-Engine/issues)

</div>

---

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ GitHub Repositories â”‚ â”€â”€â”€â–º â”‚ Markdown Extraction â”‚ â”€â”€â”€â–º â”‚ Structured OpenAI   â”‚
â”‚ (Raw Documentation) â”‚      â”‚ & Parsing Pipeline  â”‚      â”‚ Entity Extraction   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                                                     â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”                 â–¼
â”‚ Interactive         â”‚ â—„â”€â”€â”€ â”‚ NetworkX / SQLite   â”‚ â—„â”€â”€â”€ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Streamlit Explorer  â”‚      â”‚ Relational Storage  â”‚      â”‚ Pydantic Validation â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜      â”‚ Schema Guard        â”‚
                                                          â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

> Large developer codebases contain vast amounts of architectural knowledge buried inside fragmented markdown files, wikis, and issue threads, making system onboarding slow and error-prone.
> Developer Knowledge Engine automates documentation scraping, applies structured LLM extraction through strict Pydantic schemas, and builds persistent, navigable relational knowledge graphs.

---

## Features

- **Automated Repository Scraping** â€” Extracts raw markdown and documentation files directly from remote GitHub repositories.
- **LLM Entity & Relation Extraction** â€” Identifies technical concepts, architectural components, and relational dependencies with OpenAI models.
- **Zero-Hallucination Schema Guard** â€” Validates all extracted nodes and relationships against strict Pydantic models before storage.
- **Relational Knowledge Graph** â€” Constructs interconnected directed graphs using NetworkX and persists structured data in SQLite.
- **Interactive Visual Explorer** â€” Provides an intuitive Streamlit interface to search entities, inspect degrees of separation, and explore graph topology.

---

## Extraction Schema Model

The extraction pipeline enforces deterministic Pydantic schemas during OpenAI LLM invocation:

```python
class Node(BaseModel):
    entity_name: str  # Lowercase identifier
    entity_type: Literal['language', 'framework', 'database', 'tool', 'concept']

class Edge(BaseModel):
    source_entity_name: str
    target_entity_name: str
    relationship_type: Literal['uses', 'depends_on', 'alternative_to', 'improves', 'integrates_with']
    confidence_score: float = Field(ge=0.0, le=1.0)
```

---

## How It Works

```mermaid
graph LR
    A[GitHub Repo URL] --> B[GitHub Scraper & Collector]
    B --> C[Markdown Document Parser]
    C --> D[OpenAI Entity Extractor]
    D --> E[Pydantic Validation Guard]
    E --> F[NetworkX Knowledge Graph]
    F --> G[(SQLite Graph Storage)]
    F --> H[Streamlit Visual Dashboard]
```

---

## Quick Start

### Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| [Python](https://www.python.org/) | 3.10+ | Core runtime |
| [OpenAI API Key](https://platform.openai.com/) | â€” | Required for entity extraction |
| [GitHub Token](https://github.com/settings/tokens) | Optional | Avoids GitHub API rate limits |

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Justinvcj/Developer-Knowledge-Engine.git
   cd Developer-Knowledge-Engine
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Add OPENAI_API_KEY and optional GITHUB_TOKEN to .env
   ```

4. Launch the application:
   ```bash
   streamlit run main.py
   ```

### Usage

Enter a target GitHub repository URL (e.g., `https://github.com/tiangolo/fastapi`) into the Streamlit interface, trigger the extraction pipeline, and interact with the resulting knowledge graph.

---

## Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | Yes | â€” | API key for OpenAI model extraction |
| `GITHUB_TOKEN` | No | â€” | Personal access token for higher GitHub API rate limits |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Core Engine | Python 3.10+, Requests, BeautifulSoup4, Markdown |
| AI & Extraction | OpenAI API (`gpt-4o` / `gpt-3.5-turbo`), Pydantic |
| Graph & Data | NetworkX, SQLite3 |
| Interface | Streamlit |
| Testing | Pytest |

---

## Testing

```bash
# Run unit and pipeline tests
pytest test_parser.py test_extractor.py test_pipeline.py
```

---

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feat/EngineFeature`)
3. Commit your Changes (`git commit -m 'feat: add engine feature'`)
4. Push to the Branch (`git push origin feat/EngineFeature`)
5. Open a Pull Request

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
