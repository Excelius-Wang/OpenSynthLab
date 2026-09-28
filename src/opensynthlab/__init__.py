"""Template-based synthetic data generation and JSONL export."""

from .core import generate, write_jsonl

__version__ = "0.1.0a1"
__all__ = ["__version__", "generate", "write_jsonl"]
