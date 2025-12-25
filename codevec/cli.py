import sys

def help():
        print("""
Usage: vec-<command> [options]

Commands:
    index <root_path>     Index (embed) your codebase
    search <query>        Search your codebase

Examples:
    vec-index ./my-project
    vec-search "email validation"

""")

def indexer():
    """CLI entry point for indexing a codebase"""
    if len(sys.argv) < 2:
        print("Usage: vec-index <root_path>")
        print('Example: vec-index ./my-project')
        sys.exit(1)

    print("Initializing index system...")
    from codevec.index import index_codebase
    root_path = sys.argv[1]
    index_codebase(root_path)

def searcher():
    if len(sys.argv) < 2:
        print("Usage: vec-search <query>")
        print('Example: vec-search "email validation"')
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])  # Join all args in case query has spaces

    print(f"Initializing search system...")
    from codevec.search import search_code
    search_code(query)