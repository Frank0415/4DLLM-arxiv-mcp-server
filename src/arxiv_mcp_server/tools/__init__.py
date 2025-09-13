"""Tool definitions for the arXiv MCP server."""

from .search import search_tool, handle_search
from .download import download_tool, handle_download
from .list_papers import list_tool, handle_list_papers
from .read_paper import read_tool, handle_read_paper
from .cif import search_cif_tool, check_cif_tool, handle_search_cif, handle_check_cif


__all__ = [
    "search_tool",
    "download_tool",
    "read_tool",
    "search_cif_tool",
    "check_cif_tool",
    "handle_search",
    "handle_download",
    "handle_list_papers",
    "handle_read_paper",
    "handle_search_cif",
    "handle_check_cif",
    "list_tool",
]
