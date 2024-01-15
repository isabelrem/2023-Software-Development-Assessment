"""
This is a test script for select_disease.py to ensure that find_match() functions as it should
"""

# Import modules
from PanelSearch.select_disease import find_match, get_clinical_indications

# Test the find_match function from utils.select returns user-inputted disease
def test_find_match_works(monkeypatch):
    """
    Test to see if the function returns the disease.
    Monkeypatch is used to control the user input for testing purposes.
    :param monkeypatch: disease e.g. possible mitochondrial disorder - nuclear genes
    :return: disease e.g. possible mitochondrial disorder - nuclear genes
    """

    # monkeypatch the "input" function, so that it returns "Pneumothorax - familial".
    # This simulates the user entering "Pneumothorax - familial" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "possible mitochondrial disorder - nuclear genes")

    # go about using input() like you normally would:
    assert find_match("possible mitochondrial disorder - nuclear genes",
                      get_clinical_indications()) == 'possible mitochondrial disorder - nuclear genes'


# Test the find_match function from utils.select returns error
def test_find_match_errors(monkeypatch):
    """
    Test to see if function raises ValueError when disease does not exist.
    The function should return the boolean False.
    :param monkeypatch: disease not listed in National Directory e.g. jibberjabber
    :return: False
    """

    # monkeypatch the "input" function, so that it returns ValueError.
    # This simulates the user entering "jibberjabber" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "jibberjabber")

    # go about using input() like you normally would:
    assert find_match("jibberjabber", get_clinical_indications()) is False


