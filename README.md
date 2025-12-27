
<div align="center">

# Codevec

#### Codevec is the user-friendly semantic search tool for Python codebases.


![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

</div>


```bash
pip install codevec
```

## Overview

**Natural Language Search** — Find Python functions using plain English queries instead of grepping through code

**Fast** — Index, search, and get results within seconds of installing Codevec



> **Note:** Codevec currently indexes functions only. Module-level code is not included in search results.

### Why Codevec over Copilot?

**No Token Limits** — Runs entirely on lightweight local models, so you can search as much as you want without usage caps or costs

**Speed** — Often faster at finding specific functions since it's purpose-built for code search, returning results in seconds

**Privacy** — Your code never leaves your machine


## Quick Start


### 1. Index your codebase



```bash
vec-index ./your/project/file/path
```


### 2. Search with natural language

#### Run from inside the indexed codebase:
```bash
vec-search authentication logic
```

#### Run from outside the indexed codebase:
```bash
vec-search "email validation" --repo ./your-project
```


## Optional: Model server

Run the model server to keep models loaded in memory for faster searches:

```bash
vec-server  # Starts server on localhost:8000
            # Codevec will automatically use the server when available.
```

## How It Works

**Indexing** — Codevec walks your codebase to discover Python functions, then uses lightweight local models to generate embeddings

**ChromaDB Storage** — Embeddings for indexed code are stored in a ChromaDB collection located at `.codevec/` in your project root


**Re-indexing** — Simply run `vec-index` again on the same directory to update the index with new or modified functions
