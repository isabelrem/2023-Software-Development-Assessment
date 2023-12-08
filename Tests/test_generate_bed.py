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
    actual = parse_panel_data(panel_data_str)
    expected = [{'chromosome': '3', 'start': '38589547', 'end': '38691164', 'gene': 'SCN5A'}, {'chromosome': '7', 'start': '150642048', 'end': '150675403', 'gene': 'KCNH2'}, {'chromosome': '12', 'start': '21950334', 'end': '22094336', 'gene': 'ABCC9'}, {'chromosome': '4', 'start': '113739264', 'end': '114304896', 'gene': 'ANK2'}, {'chromosome': '12', 'start': '2079951', 'end': '2802108', 'gene': 'CACNA1C'}, {'chromosome': '7', 'start': '81575759', 'end': '82073114', 'gene': 'CACNA2D1'}, {'chromosome': '10', 'start': '18429605', 'end': '18830798', 'gene': 'CACNB2'}, {'chromosome': '3', 'start': '8775485', 'end': '8883492', 'gene': 'CAV3'}, {'chromosome': '3', 'start': '196769430', 'end': '197026171', 'gene': 'DLG1'}, {'chromosome': '3', 'start': '32147180', 'end': '32210205', 'gene': 'GPD1L'}, {'chromosome': '15', 'start': '73612199', 'end': '73661605', 'gene': 'HCN4'}, {'chromosome': '1', 'start': '112313283', 'end': '112531777', 'gene': 'KCND3'}, {'chromosome': '11', 'start': '74165885', 'end': '74178774', 'gene': 'KCNE3'}, {'chromosome': 'X', 'start': '108866928', 'end': '108868393', 'gene': 'KCNE5'}, {'chromosome': '12', 'start': '21917888', 'end': '21928515', 'gene': 'KCNJ8'}, {'chromosome': '12', 'start': '32943678', 'end': '33049774', 'gene': 'PKP2'}, {'chromosome': '17', 'start': '8191814', 'end': '8193410', 'gene': 'RANGRF'}, {'chromosome': '3', 'start': '38738292', 'end': '38835501', 'gene': 'SCN10A'}, {'chromosome': '19', 'start': '35521587', 'end': '35531352', 'gene': 'SCN1B'}, {'chromosome': '11', 'start': '118032665', 'end': '118047388', 'gene': 'SCN2B'}, {'chromosome': '11', 'start': '123499894', 'end': '123525952', 'gene': 'SCN3B'}, {'chromosome': '3', 'start': '57741176', 'end': '57914895', 'gene': 'SLMAP'}, {'chromosome': '19', 'start': '49660997', 'end': '49715093', 'gene': 'TRPM4'}]
    assert actual == expected


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
    beds = parse_panel_data(panel_data_str)
    filename = "test_bed_filename"
    actual = write_bed_file(beds, filename)
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

    # Test write_bed_file function
    beds = parse_panel_data(panel_data_str)
    filename = None
    actual = write_bed_file(beds, filename)
    expected = (False, 'Error writing files: expected str, bytes or os.PathLike object, not NoneType')
    assert actual == expected


def test_write_bed_file_no_beds():
    """
    Tests the function to see if it can capture errors
    """

    # Test write_bed_file function
    beds = None
    filename = "test_bed_filename"
    actual = write_bed_file(beds, filename)
    expected = (False, "Error writing files: 'NoneType' object is not iterable")
    assert actual == expected