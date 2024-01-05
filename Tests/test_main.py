"""
Test main.py functions
"""

# Import functions and packages
from PanelSearch.main import *
import pytest

# Test get_genome_build() works
def test_get_genome_build_works(monkeypatch):
    """
    Test to see if the function returns the genome build.
    Monkeypatch is used to control the user input for testing purposes.
    :param monkeypatch: user input e.g. 1
    :return: genome build e.g. GRch37
    """
    monkeypatch.setattr('builtins.input', lambda _: "1")
    mock = PanelSearch()
    assert mock.get_genome_build() == 'GRch37'

# Test get_genome_build() errors
def test_get_genome_build_errors(monkeypatch):
        """
        Test to see if the function returns ValueError.
        Monkeypatch is used to control the user input for testing purposes.
        :param monkeypatch: user input e.g. 3
        :return: ValueError
        """
        with pytest.raises(ValueError):
            monkeypatch.setattr('builtins.input', lambda _: "3")
            mock = PanelSearch()
            mock.get_genome_build()


# Test get_input_string_type() works
def test_get_input_string_type_works(monkeypatch):
    """
    Test to see if the function returns the user input type.
    Monkeypatch is used to control the user input for testing purposes.
    :param monkeypatch: user input e.g. 1
    :return: R-code option
    """
    monkeypatch.setattr('builtins.input', lambda _: "1")
    mock = PanelSearch()
    assert mock.get_input_string_type() == 'R-code'


# Test get_input_string_type() errors
def test_get_input_string_type_errors(monkeypatch):
        """
        Test to see if the function returns ValueError.
        Monkeypatch is used to control the user input for testing purposes.
        :param monkeypatch: user input e.g. 3
        :return: ValueError
        """
        with pytest.raises(ValueError):
            monkeypatch.setattr('builtins.input', lambda _: "3")
            mock = PanelSearch()
            mock.get_input_string_type()


# Test get_input_string() works
def test_get_input_string(monkeypatch):
    """
    Test to see if the function returns the user input.
    Monkeypatch is used to control the user input for testing purposes.
    :param monkeypatch: user input e.g. R128
    :return: R128
    """
    monkeypatch.setattr('builtins.input', lambda _: "1") # Runs get_input_string_type() first
    mock = PanelSearch()
    monkeypatch.setattr('builtins.input', lambda _: "R128")  # Test get_input_string()
    assert mock.get_input_string() == 'R128'


# Test create_bed_filename() works
def test_create_bed_filename():
    """
    BED file created with gene panel name and genome build
    :return: 'bed_files\\R128_GRCh37_20231128.bed'
    """
    assert type(create_bed_filename('R128', 'GRCh37')) == str
