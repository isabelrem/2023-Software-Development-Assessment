import pytest
import json
import os
import sys

# Adjust the system path so the script can be imported
sys.path.append('/home/egleg/PycharmProjects/panel/2023-Software-Development-Assessment/PanelSearch')

from generate_bed import parse_panel_data, write_bed_file  # Import the functions to be tested

# Sample valid JSON input for parse_panel_data
valid_json_data = json.dumps({
    "Genes": [
        {"HGNC:1": ["Gene1", ["1", "100-200"]]},
        {"HGNC:2": ["Gene2", ["X", "300-400"]]}
    ]
})

# Sample expected output for parse_panel_data
expected_beds = [
    {'chromosome': '1', 'start': '99', 'end': '200', 'gene': 'Gene1'},
    {'chromosome': 'X', 'start': '299', 'end': '400', 'gene': 'Gene2'}
]

def test_parse_panel_data_valid():
    """ Test parsing valid JSON data """
    assert parse_panel_data(valid_json_data) == expected_beds

def test_parse_panel_data_invalid():
    """ Test parsing invalid JSON data """
    with pytest.raises(SystemExit):
        parse_panel_data("Invalid JSON")

def test_write_bed_file(tmp_path):
    """ Test writing BED and JSON files """
    filename = tmp_path / "test.bed"
    success, message = write_bed_file(expected_beds, str(filename))
    assert success
    assert message == "Success"
    assert os.path.isfile(filename)
    assert os.path.isfile(str(filename).replace('.bed', '.json'))