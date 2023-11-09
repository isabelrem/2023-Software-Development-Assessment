"""
This is a test script for select.py to ensure that find_match() functions as it should
"""

# Import modules
from utils.select import find_match, clinical_indications


# Test the find_match function from utils.select returns user-inputted disease
def test_function_works(monkeypatch):
    """
    Test to see if the function returns the disease.
    Monkeypatch is used to control the user input for testing purposes.
    :param monkeypatch: disease e.g. Pneumothorax - familial
    :return: disease e.g. Pneumothorax - familial
    """

    # monkeypatch the "input" function, so that it returns "Pneumothorax - familial".
    # This simulates the user entering "Pneumothorax - familial" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "Pneumothorax - familial")

    # go about using input() like you normally would:
    assert find_match("Pneumothorax - familial", clinical_indications) == 'Pneumothorax - familial'


# Test the find_match function from utils.select returns error
def test_function_errors(monkeypatch):
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
    assert find_match("jibberjabber", clinical_indications) is False


