"""
Functional test to test app runs by connection to API's and SQL database
"""

# import pytest
from PanelSearch.main import *

# @pytest.mark.functional
# def test_print_name(new, rcode, term, build, bed, exon, padding, save, ID):
#     main()

# To run
# py.test -s ./Tests/functional.py

def test_say_hello(monkeypatch):
    inputs = iter(['1', '1', 'R128', '1', 'Y', 'Y', 'Tester'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = main()
    assert result == "Thank you for using PanelSearch. Goodbye."

# To run
# pytest ./Tests/functional.py