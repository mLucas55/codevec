import sys

def help():
        print("""
Usage: vec-<command> [options]

Commands:
    index <root_path>     Index (embed) your codebase
    search <query>        Search your codebase
    config                Configure settings

Examples:
    vec-index ./my-project
    vec-search "email validation"
    vec-config

""")

def indexer():
    """CLI entry point for indexing a codebase"""
    if len(sys.argv) < 2:
        print("Usage: vec-index <root_path>")
        print('Example: vec-index ./my-project')
        sys.exit(1)
    
    from codevec.index import index_codebase
    root_path = sys.argv[1]
    index_codebase(root_path)

def searcher():
    if len(sys.argv) < 2:
        print("Usage: vec-search <query>")
        print('Example: vec-search "email validation"')
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])  # Join all args in case query has spaces

    from codevec.search import search_code
    search_code(query)

def configurator():
    """CLI entry point for configuring settings"""
    from codevec.config import configure_model, configure_api_key, configure_reranking, get_model_type, get_reranking
    
    print("CodeVec Configuration")
    print("=" * 50)
    print("\nWhat would you like to configure?")
    print("  1. Embedding model")
    print("  2. Reranking")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        _configure_embedding_model(configure_model, configure_api_key, get_model_type)
    elif choice == "2":
        _configure_reranking(configure_reranking, get_reranking)
    else:
        print("\n✗ Error: Invalid choice. Please enter 1 or 2")
        sys.exit(1)


def _configure_embedding_model(configure_model, configure_api_key, get_model_type):
    """Configure the embedding model"""
    current = get_model_type()
    print(f"\nCurrent embedding model: {current}")
    print("\nChoose embedding model:")
    print("  1. Local (sentence-transformers)")
    print("  2. Gemini (Google AI)")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        configure_model("local")
        print("\n✓ Configuration saved: Using local embeddings")
    elif choice == "2":
        configure_model("gemini")
        api_key = input("\nEnter your Gemini API key: ").strip()
        if api_key:
            configure_api_key(api_key)
            print("\n✓ Configuration saved: Using Gemini embeddings")
        else:
            print("\n✗ Error: API key cannot be empty")
            sys.exit(1)
    else:
        print("\n✗ Error: Invalid choice. Please enter 1 or 2")
        sys.exit(1)


def _configure_reranking(configure_reranking, get_reranking):
    """Configure reranking on/off"""
    current = get_reranking()
    status = "on" if current else "off"
    print(f"\nReranking is currently: {status}")
    print("\nReranking improves result quality but adds latency.")
    print("  1. On")
    print("  2. Off")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        configure_reranking("True")
        print("\n✓ Configuration saved: Reranking enabled")
    elif choice == "2":
        configure_reranking("False")
        print("\n✓ Configuration saved: Reranking disabled")
    else:
        print("\n✗ Error: Invalid choice. Please enter 1 or 2")
        sys.exit(1)