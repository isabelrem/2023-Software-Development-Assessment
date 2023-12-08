"""
Tests functions from VV_API_Request.py
"""

# Import local functions from PanelSearch folder and pytest module
from PanelSearch.VV_API_Request import *
import pytest

# Test genome_build_convert works
def test_genome_build_convert_GRch37():
    """
    Change lowercase c to capital c in GRCh37/8 for VariantValidator API formatting
    (PanelApp API requires lowercase)
    :return: genome build
    """
    mock = VVRequest('GRch37')
    assert mock.genome_build_convert('GRch37') == 'GRCh37'


# Test genome_build_convert fails
def test_genome_build_convert_fails():
    """
    Wrong input results in ValueError
    :return: ValueError
    """
    with pytest.raises(ValueError):
        VVRequest('blah')


# Test request_data works:
def test_request_data_works():
    """
    request_data() is a skeleton for gene_to_transcripts()
    :return: requests.models.Response
    """
    mock = VVRequest('GRch37')
    mock.gene_to_transcripts('HGNC:4982', 'refseq')  # requires gene_to_transcripts for URL
    assert type(mock.request_data()) == requests.models.Response


# Test gene_to_transcripts works
def test_gene_to_transcripts_works():
    """
    Make a request to the VV API gene2transcript v2 endpoint to get back MANE select transcripts
    :return: requests.models.Response
    """
    mock = VVRequest('GRch37')
    mock_request = mock.gene_to_transcripts('HGNC:4982', 'refseq')
    assert type(mock_request) == requests.models.Response
