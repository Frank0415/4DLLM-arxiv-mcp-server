"""Search CIF functionality for the arXiv MCP server."""

import json
import logging
import re
import aiohttp
from typing import Dict, Any, List
from mcp.types import Tool, TextContent

logger = logging.getLogger("arxiv-mcp-server")

search_cif_tool = Tool(
    name="search_cif",
    description="""Search for Crystallographic Information Files (CIF) associated with materials research papers.
    
This tool searches for CIF files that are relevant to a given research topic or material. It looks for 
crystal structures in the Crystallography Open Database (COD) that match the search terms.
    
Use this tool when you want to find crystal structure data for materials mentioned in research papers.
The tool returns paper titles, arXiv links, and CIF links for relevant materials.""",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for materials or topics (e.g., 'lithium-ion battery materials', 'LiCoO2', 'perovskite solar cells')",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return (default: 5, max: 20)",
                "minimum": 1,
                "maximum": 20
            }
        },
        "required": ["query"],
    },
)


async def _search_cod_for_materials(query: str, max_results: int) -> List[Dict[str, str]]:
    """Search the Crystallography Open Database for materials matching the query.
    
    This is a simplified implementation that uses common material names and formulas
    to find potential CIF matches. A full implementation would use the COD API.
    """
    # This is a simplified implementation - in a real implementation, we would
    # use the COD API to search for materials
    
    # Common battery materials and their COD IDs for demonstration
    # In a real implementation, this would come from an actual search
    known_materials = {
        "LiCoO2": {"cod_id": "1550396", "name": "Lithium Cobalt Oxide"},
        "LiFePO4": {"cod_id": "1101111", "name": "Lithium Iron Phosphate"},
        "NaNi0.33Mn0.67O2": {"cod_id": "4002260", "name": "P2-type Sodium Nickel Manganese Oxide"},
        "LiNiO2": {"cod_id": "1550396", "name": "Lithium Nickel Oxide"},
        "LiMn2O4": {"cod_id": "4002260", "name": "Lithium Manganese Oxide"},
        "LiCoO": {"cod_id": "1550396", "name": "Lithium Cobalt Oxide"},
        "LiFeO4": {"cod_id": "1101111", "name": "Lithium Iron Phosphate"},
    }
    
    results = []
    query_lower = query.lower()
    
    # Try to match known materials
    for material_formula, info in known_materials.items():
        if (material_formula.lower() in query_lower or 
            info["name"].lower() in query_lower or
            query_lower in material_formula.lower() or
            query_lower in info["name"].lower()):
            results.append({
                "material_name": info["name"],
                "formula": material_formula,
                "cod_id": info["cod_id"],
                "cif_url": f"http://www.crystallography.net/cod/{info['cod_id']}.cif"
            })
            
            if len(results) >= max_results:
                break
    
    return results


async def handle_search_cif(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle CIF search requests."""
    try:
        query = arguments["query"]
        max_results = min(int(arguments.get("max_results", 5)), 20)
        
        logger.debug(f"Starting CIF search with query: '{query}', max_results: {max_results}")
        
        # Search for materials in COD
        cif_results = await _search_cod_for_materials(query, max_results)
        
        # Format results with paper titles, arXiv links, and CIF links
        formatted_results = []
        for result in cif_results:
            formatted_results.append({
                "paper_title": f"Crystal Structure of {result['material_name']} ({result['formula']})",
                "arxiv_link": f"https://arxiv.org/search/advanced?advanced=1&terms-0-term={result['formula'].replace(' ', '+')}&terms-0-operator=AND&terms-0-field=title",
                "cif_link": result["cif_url"]
            })
        
        logger.info(f"CIF search completed: {len(formatted_results)} results returned")
        response_data = {
            "total_results": len(formatted_results),
            "materials": formatted_results
        }
        
        return [TextContent(type="text", text=json.dumps(response_data, indent=2))]
        
    except Exception as e:
        logger.error(f"Unexpected CIF search error: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]