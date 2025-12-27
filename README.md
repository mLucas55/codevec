
<div align="center">

# Codevec

#### Codevec is the user-friendly semantic search tool for Python codebases.


![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

</div>


```bash
pip install codevec
```

## Overview

Codevec is a semantic search tool for Python codebases that lets you find functions using plain English queries, no need to know exact function names or keywords to grep.

It runs entirely on lightweight local models, so your code never leaves your machine. There are no API calls, usage limits, or external dependencies, and indexing a codebase takes only seconds.

Unlike general-purpose AI assistants, Codevec is purpose-built for code search. It focuses on quickly pinpointing relevant function definitions without verbose explanations, making it especially effective for navigating large or unfamiliar repositories.

> **Note:** Codevec currently indexes Python functions only. Module-level code is not indexed.


## Quick Start


### 1. Index your codebase



```bash
vec-index ./your/project/filepath
```
> **Note:** Don't forget to re-index after big changes!

### 2. Search with natural language

#### Run from inside the indexed codebase:
```bash
vec-search email validation
```

#### Run from outside the indexed codebase:
```bash
vec-search "authentication logic" --repo ./your/project/filepath
```
### 3. Example results
```
(.venv) user@Computer demo-repo % vec-search email validation
Initializing search system...
Found 5 results

================================================================================

┌─ Result #1 ───────────────────────────────────────────────────────────
│ Similarity: 49.3%  │  Rerank: -2.527
├───────────────────────────────────────────────────────────────────────────────
│ 📁 File: /Users/user/development/project/utils/validation.py
│ ⚙️ Function: validate_email (line 5)
├───────────────────────────────────────────────────────────────────────────────
│ Code:
│    5 │ def validate_email(email):
│    6 │     """Check if email address is in valid format"""
│    7 │     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
│    8 │     return re.match(pattern, email) is not None
└───────────────────────────────────────────────────────────────────────────────
```

> **Note:** The filepath is clickable in VS Code terminals!

## Optional: Model server

Run the model server to keep models loaded in memory for faster searches:

```bash
vec-server  # Starts server on localhost:8000
            # Codevec will automatically use the server when available
```

## How It Works

**Indexing & Embedding** — Codevec walks your codebase and uses AST parsing to discover Python functions, then uses a lightweight local transformer to generate embeddings

**ChromaDB Storage** — Embeddings are stored in a ChromaDB collection located at `.codevec/` in your project root

**Searching** — Queries are embedded and matched against ChromaDB using semantic similarity, then results are reranked using a cross-encoder for improved relevance

**Re-indexing** — Simply run `vec-index` again on the same directory to update the index with new or modified functions
