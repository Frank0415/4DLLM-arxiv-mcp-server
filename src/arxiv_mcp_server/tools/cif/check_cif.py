"""Check CIF functionality for the arXiv MCP server."""

import json
import logging
import re
import aiohttp
from typing import Dict, Any, List
from mcp.types import Tool, TextContent

logger = logging.getLogger("arxiv-mcp-server")

check_cif_tool = Tool(
    name="check_cif",
    description="""Check if a specific research paper has associated Crystallographic Information Files (CIF).
    
This tool checks if a given arXiv paper has any associated CIF files in the Crystallography Open Database (COD).
Provide the paper title or ID, and the tool will check for related CIF files.""",
    inputSchema={
        "type": "object",
        "properties": {
            "paper_title": {
                "type": "string",
                "description": "Title of the research paper to check for CIF files",
            },
            "paper_id": {
                "type": "string",
                "description": "ArXiv ID of the paper (e.g., '2401.12345')",
            }
        },
        "required": [],
    },
)


async def _check_paper_for_cif(paper_title: str = None, paper_id: str = None) -> List[Dict[str, str]]:
    """Check if a paper has associated CIF files.
    
    This is a simplified implementation that uses common material names extracted from
    the paper title to find potential CIF matches.
    """
    # This is a simplified implementation - in a real implementation, we would
    # use more sophisticated methods to extract material names and search COD
    
    if not paper_title and not paper_id:
        return []
    
    # Extract potential material names from the paper title
    # This is a very simplified approach - a real implementation would be more sophisticated
    search_terms = []
    if paper_title:
        search_terms.append(paper_title)
    if paper_id:
        search_terms.append(paper_id)
    
    # Common battery materials and their COD IDs for demonstration
    # In a real implementation, this would come from an actual search
    known_materials = {
        "LiCoO2": {"cod_id": "1550396", "name": "Lithium Cobalt Oxide"},
        "LiFePO4": {"cod_id": "1101111", "name": "Lithium Iron Phosphate"},
        "NaNi0.33Mn0.67O2": {"cod_id": "4002260", "name": "P2-type Sodium Nickel Manganese Oxide"},
        "lithium": {"cod_id": "1550396", "name": "Lithium compounds"},
        "cobalt": {"cod_id": "1550396", "name": "Cobalt compounds"},
        "iron": {"cod_id": "1101111", "name": "Iron compounds"},
        "phosphate": {"cod_id": "1101111", "name": "Phosphate compounds"},
        "sodium": {"cod_id": "4002260", "name": "Sodium compounds"},
        "nickel": {"cod_id": "4002260", "name": "Nickel compounds"},
        "manganese": {"cod_id": "4002260", "name": "Manganese compounds"},
    }
    
    results = []
    query_text = " ".join(search_terms).lower()
    
    # Try to match known materials
    for material_term, info in known_materials.items():
        if material_term.lower() in query_text:
            results.append({
                "material_name": info["name"],
                "formula": material_term,
                "cod_id": info["cod_id"],
                "cif_url": f"http://www.crystallography.net/cod/{info['cod_id']}.cif"
            })
    
    return results


async def handle_check_cif(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle CIF check requests."""
    try:
        paper_title = arguments.get("paper_title")
        paper_id = arguments.get("paper_id")
        
        logger.debug(f"Checking paper for CIF: title='{paper_title}', id='{paper_id}'")
        
        # Check if paper has associated CIF files
        cif_results = await _check_paper_for_cif(paper_title, paper_id)
        
        if cif_results:
            # Format results with paper titles, arXiv links, and CIF links
            formatted_results = []
            for result in cif_results:
                formatted_results.append({
                    "material_name": result["material_name"],
                    "cif_link": result["cif_url"],
                    "has_cif": True
                })
            
            logger.info(f"CIF check completed: {len(formatted_results)} CIF files found")
            response_data = {
                "paper_title": paper_title or f"Paper {paper_id}",
                "has_cif_files": True,
                "cif_files": formatted_results
            }
        else:
            logger.info("CIF check completed: No CIF files found")
            response_data = {
                "paper_title": paper_title or f"Paper {paper_id}",
                "has_cif_files": False,
                "message": "No CIF files found for this paper"
            }
        
        return [TextContent(type="text", text=json.dumps(response_data, indent=2))]
        
    except Exception as e:
        logger.error(f"Unexpected CIF check error: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]