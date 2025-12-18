# codebase-semantic-search

A semantic search tool for Python codebases using AI embeddings. Index your code once, then search using natural language to find relevant functions instantly. Powered by Google Gemini embeddings and ChromaDB vector storage. Can be quickly modified to support locally hosted embedding models as well.

**Quick Start:**
```bash
# Index your codebase
python index.py ./your-project

# Search with natural language
python search.py "authentication logic"
python search.py "calculate factorial"
```