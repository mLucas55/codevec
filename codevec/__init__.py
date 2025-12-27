"""CodeVec: Semantic code search using embeddings.

This package provides tools for indexing and searching codebases using
embeddings, enabling natural language queries over your code.
"""

__version__ = "1.0.1"

# Lazy imports to avoid loading heavy dependencies at package import time
def __getattr__(name):
    """Lazy attribute loader for heavy dependencies.
    
    Args:
        name: The attribute name to load
        
    Returns:
        The requested attribute
        
    Raises:
        AttributeError: If the attribute doesn't exist
    """
    if name == "indexer":
        from .cli import indexer
        return indexer
    elif name == "searcher":
        from .cli import searcher
        return searcher
    elif name == "show_help":
        from .cli import show_help
        return show_help
    elif name == "run_server":
        from .cli import run_server
        return run_server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["indexer", "searcher", "show_help", "run_server", "__version__"]