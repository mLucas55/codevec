# codevec

Codevec is a semantic search tool for finding python functions in your codebases. Index and embed your codebase, then search for functions using natural language to find relevant results in seconds.

## Installation

```bash
pip install codevec
```

## Quick Start

```bash
# Index your codebase
vec-index ./your-project

# Search with natural language  
vec-search authentication logic
vec-search "email validation" --repo ./your-project
```

## Optional: Run embedding server

For faster repeated searches, run the embedding server to keep models loaded in memory:

```bash
vec-server  # Starts server on localhost:8000
```

Codevec will automatically use the server when available.