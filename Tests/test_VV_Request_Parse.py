"""
Tests vv_request_parse function from VV_Request_Parse.py
"""

# Import local modules
from PanelSearch.VV_Request_Parse import *
from PanelSearch.PanelApp_Request_Parse import *
from PanelSearch.PanelApp_API_Request import *
import json
import pytest
from PanelSearch.VV_API_Request import *

# Test vv_request_parse works
def test_vv_request_parse():
    """
    Parses the response of a gene2transcripts request to VV API, adds transcript info to panel_dict
    :return: dictionary of PanelApp API results and VV transcripts
    """
    # Create PanelApp API dictionary
    data = PanelAppRequest()
    mock_request = data.pk_search('Brugada syndrome and cardiac sodium channel disease')
    parsed = panelapp_search_parse(mock_request.json(), 'GRch37')

    # Get VV API transcripts
    mock = VVRequest('GRch37')
    mock_request = mock.gene_to_transcripts('HGNC:4982', 'refseq')

    # Add VV data to PanelApp dictionary
    result = vv_request_parse(mock_request.json(), parsed)
    assert type(result) == dict
