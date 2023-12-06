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

    # Get Mane_Select Transcripts for each gene:
    # Get the gene id's in a list:
    gene_list = []
    for gene_dict in parsed['Genes']:
        gene_list += list(gene_dict.keys())

    # Put id's in query from for VV API:
    vv_genes_query = ''
    vv_genes_query += gene_list[0]
    if len(gene_list) > 1:
        for gene_id in gene_list[1:]:
            vv_genes_query += f'|{gene_id}'

    vv_genes_query = vv_genes_query.strip()

    print(f'HGNC list: {vv_genes_query}')

    # Perform a query to the VV API for that list:
    VV_REQ = VVRequest('GRch37')
    VV_RESP = VV_REQ.gene_to_transcripts(vv_genes_query, 'refseq')

    # Add VV data to PanelApp dictionary
    if VV_RESP.status_code == 200:
        parsed = vv_request_parse(VV_RESP.json(), parsed)

    # Check output
    assert type(parsed) == dict
