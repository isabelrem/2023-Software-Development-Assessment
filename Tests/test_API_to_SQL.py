"""
Tests for API_to_SQL.py functions
"""

# Import functions
from PanelSearch.API_to_SQL import *
import pytest

def test_PK_Parse_Data_to_SQL_works():
    """
    Test with R128 panel ID, GRCh37 build, and R128 panel name
    """
    result = PK_Parse_Data_to_SQL("13", "GRch37", "Brugada syndrome and cardiac sodium channel disease")
    assert result == 13


def test_PK_Parse_Data_to_SQL_type_errors():
    """
    Test with missing inputs
    """ 
    with pytest.raises(TypeError):
        PK_Parse_Data_to_SQL()
    

def test_PK_Parse_Data_to_SQL_value_errors():
    """
    Test with missing inputs
    """ 
    with pytest.raises(ValueError):
        PK_Parse_Data_to_SQL(34, 56, 71)
