"""
Tests for generate_bed.py functions
"""

# Import packages
from PanelSearch.generate_bed import *
from PanelSearch.main import *


# Test parse_panel_data() works
def test_parse_panel_data():
    """
    Tests the function to see if it can produce a dictionary with BED data
    """
    # Create JSON from variant validator request
    request = PanelAppRequest()
    response = request.r_search('R128')
    panel_data = panelapp_search_parse(response.json(), 'GRch37')
    panel_data_str = json.dumps(panel_data)

    # Test parse_panel_data function
    actual = parse_panel_data(panel_data_str, "gen", 7)
    assert type(actual) == list


# Test write_bed_file() works
def test_write_bed_file_works():
    """
    Tests the function to see if it can produce a BED file
    """
    # Create JSON from variant validator request
    request = PanelAppRequest()
    response = request.r_search('R128')
    panel_data = panelapp_search_parse(response.json(), 'GRch37')
    panel_data_str = json.dumps(panel_data)

    # Test write_bed_file function
    beds = parse_panel_data(panel_data_str, 'gen', 7)
    filename = 'test_bed_filename'
    actual = write_bed_file(beds, filename, 'gen', 'GRch37')
    expected = (True, 'Success')
    assert actual == expected


# Test write_bed_file() captures errors
def test_write_bed_file_no_filename():
    """
    Tests the function to see if it can capture errors
    """
    # Create JSON from variant validator request
    request = PanelAppRequest()
    response = request.r_search('R128')
    panel_data = panelapp_search_parse(response.json(), 'GRch37')
    panel_data_str = json.dumps(panel_data)

    # Test write_bed_file function
    beds = parse_panel_data(panel_data_str, 'gen', 7)
    filename = None
    actual = write_bed_file(beds, filename, 'gen', 7)
    expected = (False, "Error writing files: expected str, bytes or os.PathLike object, not NoneType")
    assert actual == expected


def test_write_bed_file_no_beds():
    """
    Tests the function to see if it can capture errors
    """

    # Test write_bed_file function
    beds = None
    filename = "test_bed_filename"
    actual = write_bed_file(beds, filename, 'gen', 7)
    expected = (False, "Error writing files: 'NoneType' object is not iterable")
    assert actual == expected
