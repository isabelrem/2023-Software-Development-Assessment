"""
Functional test to test app runs by connection to API's and SQL database
"""
# Import function main() from PanelSearch/main.py
from PanelSearch.main import *

# Test main() works
def test_main_new_search(monkeypatch):
    """
    Try new search with r-code R128 and build GRCh37. Save BED file in SQL database with patient ID Tester.
    """
    inputs = iter(['1', '1', 'R128', '1', 'Y', 'Y', 'Tester'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = main()
    assert result == "Thank you for using PanelSearch. Goodbye."


def test_main_old_search(monkeypatch):
    """
    Find old records and save CSV file locally.
    """
    inputs = iter(['2', 'Patient 1', 'Y', 'test'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = main()
    assert result == "Thank you for using PanelSearch. Goodbye."

# To run standalone from root directory
# pytest ./Tests/functional.py