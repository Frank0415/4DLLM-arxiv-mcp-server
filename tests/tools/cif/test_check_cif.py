"""Tests for the check_cif tool."""

import pytest
from arxiv_mcp_server.tools.cif.check_cif import handle_check_cif


@pytest.mark.asyncio
async def test_check_cif_with_title():
    """Test checking CIF files for a paper with title."""
    arguments = {
        "paper_title": "Lithium Cobalt Oxide for Battery Applications"
    }
    
    result = await handle_check_cif(arguments)
    
    # Check that we get a result
    assert len(result) == 1
    assert result[0].type == "text"
    
    # Parse the JSON response
    import json
    response_data = json.loads(result[0].text)
    
    # Check that we have the expected structure
    assert "paper_title" in response_data
    assert "has_cif_files" in response_data


@pytest.mark.asyncio
async def test_check_cif_with_id():
    """Test checking CIF files for a paper with ID."""
    arguments = {
        "paper_id": "2401.12345"
    }
    
    result = await handle_check_cif(arguments)
    
    # Check that we get a result
    assert len(result) == 1
    assert result[0].type == "text"
    
    # Parse the JSON response
    import json
    response_data = json.loads(result[0].text)
    
    # Check that we have the expected structure
    assert "paper_title" in response_data
    assert "has_cif_files" in response_data


@pytest.mark.asyncio
async def test_check_cif_with_both_parameters():
    """Test checking CIF files with both title and ID."""
    arguments = {
        "paper_title": "Sodium-ion Battery Materials",
        "paper_id": "2402.67890"
    }
    
    result = await handle_check_cif(arguments)
    
    # Check that we get a result
    assert len(result) == 1
    assert result[0].type == "text"
    
    # Parse the JSON response
    import json
    response_data = json.loads(result[0].text)
    
    # Check that we have the expected structure
    assert "paper_title" in response_data
    assert "has_cif_files" in response_data