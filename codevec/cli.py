import sys

def help():
        print("""
Usage: vec-<command> [options]

Commands:
    index <path>              Index a codebase (creates .codevec/ in the target)
    search <query> [options]  Search indexed code

Search Options:
    --repo <path>             Search a specific repository (default: auto-detect)

Examples:
    vec-index ./my-project
    cd my-project && vec-search "email validation"
    vec-search "email validation" --repo ./my-project

""")

def indexer():
    """CLI entry point for indexing a codebase"""
    if len(sys.argv) < 2:
        print("Usage: vec-index <path>")
        print('Example: vec-index ./my-project')
        sys.exit(1)

    print("Initializing index system...")
    from codevec.index import index_codebase
    root_path = sys.argv[1]
    index_codebase(root_path)

def searcher():
    """CLI entry point for searching indexed code"""
    if len(sys.argv) < 2:
        print("Usage: vec-search <query> [--repo <path>]")
        print('Example: vec-search "email validation"')
        print('Example: vec-search "email validation" --repo ./my-project')
        sys.exit(1)
    
    # Parse arguments
    args = sys.argv[1:]
    root_path = None
    query_parts = []
    
    i = 0
    while i < len(args):
        if args[i] == "--repo" and i + 1 < len(args):
            root_path = args[i + 1]
            i += 2
        else:
            query_parts.append(args[i])
            i += 1
    
    if not query_parts:
        print("Error: No search query provided")
        sys.exit(1)
    
    query = " ".join(query_parts)

    print(f"Initializing search system...")
    from codevec.search import search_code
    search_code(query, root_path=root_path)