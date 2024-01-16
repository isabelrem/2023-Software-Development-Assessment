"""
Tests Panel_App_Request_Parse.py functions
"""

# Import functions from file
from PanelSearch.PanelApp_Request_Parse import *
from PanelSearch.PanelApp_API_Request import *
import json
import pytest


# Test that panelapp_search_parse works
def test_panelapp_search_parse_works():
    """
    If genome build is correct then the API output is parsed as a dictionary
    :return: dictionary of API output
    """
    data = PanelAppRequest()
    mock_request = data.pk_search('Brugada syndrome and cardiac sodium channel disease')
    parsed = panelapp_search_parse(mock_request.json(), 'GRch37')
    assert type(parsed) == dict


# Test that panelapp_search_parse fails
def test_panelapp_search_parse_fails():
    """
    If genome build is invalid then ValueError raised
    :return: ValueError
    """
    with pytest.raises(ValueError):
        data = PanelAppRequest()
        mock_request = data.pk_search('Fetal anomalies with a likely genetic cause')
        panelapp_search_parse(mock_request.json(), 'blah')

