__version__ = "1.0.0"

# Lazy imports to avoid loading heavy dependencies at package import time
def __getattr__(name):
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