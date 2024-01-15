"""
Test for PanelApp_API_Request
"""

# Import functions and pytest module
from PanelSearch.PanelApp_API_Request import *
import pytest

# Test request_data method
def test_request_data():
    """
    This function is used for the pk_search method
    :return: requests.exceptions.MissingSchema
    """
    data = PanelAppRequest()
    data.pk_search('Fetal anomalies with a likely genetic cause')  # need this for request_data to work
    assert type(data.request_data()) == requests.models.Response


# Test pk_search method
def test_pk_search():
    """
    This function should return gene list from panelApp API
    :return: requests.models.Response
    """
    data = PanelAppRequest()
    mock_request = data.pk_search('Fetal anomalies with a likely genetic cause')
    assert type(mock_request) == requests.models.Response


# Test r_search method works
def test_r_search_works():
    """
    This function should return panelApp API data from entering an R-code
    :return: requests.models.Response
    """
    data = PanelAppRequest()
    mock_request = data.r_search('R128')
    assert type(mock_request) == requests.models.Response


# Test r_search method fails
def test_r_search_fails():
    """
    This function should return panelApp API data from entering an R-code
    :return: ValueError
    """
    with pytest.raises(ValueError):
        data = PanelAppRequest()
        data.r_search('R128453')

