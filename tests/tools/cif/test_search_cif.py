"""Tests for the search_cif tool."""

import pytest
from arxiv_mcp_server.tools.cif.search_cif import handle_search_cif


@pytest.mark.asyncio
async def test_search_cif_basic():
    """Test basic CIF search functionality."""
    arguments = {
        "query": "LiCoO2",
        "max_results": 5
    }
    
    result = await handle_search_cif(arguments)
    
    # Check that we get a result
    assert len(result) == 1
    assert result[0].type == "text"
    
    # Parse the JSON response
    import json
    response_data = json.loads(result[0].text)
    
    # Check that we have the expected structure
    assert "total_results" in response_data
    assert "materials" in response_data
    assert isinstance(response_data["total_results"], int)
    assert isinstance(response_data["materials"], list)


@pytest.mark.asyncio
async def test_search_cif_with_different_material():
    """Test CIF search with a different material."""
    arguments = {
        "query": "LiFePO4",
        "max_results": 3
    }
    
    result = await handle_search_cif(arguments)
    
    # Check that we get a result
    assert len(result) == 1
    assert result[0].type == "text"
    
    # Parse the JSON response
    import json
    response_data = json.loads(result[0].text)
    
    # Check that we have results
    assert isinstance(response_data["total_results"], int)
    assert isinstance(response_data["materials"], list)


@pytest.mark.asyncio
async def test_search_cif_max_results_limit():
    """Test that max_results parameter is respected."""
    arguments = {
        "query": "lithium battery",
        "max_results": 2
    }
    
    result = await handle_search_cif(arguments)
    
    # Check that we get a result
    assert len(result) == 1
    assert result[0].type == "text"
    
    # Parse the JSON response
    import json
    response_data = json.loads(result[0].text)
    
    # Check that we don't exceed the max results
    assert response_data["total_results"] <= 2
    assert len(response_data["materials"]) <= 2