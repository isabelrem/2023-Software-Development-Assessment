"""
Test functions from SQL_Functions.py
"""

# import functions
from PanelSearch.SQL_Functions import *
import sqlalchemy
import pandas
import re


def test_connect_db_works():
    """
    Test connect_db() function creates engine
    """
    actual = connect_db()
    assert type(actual) == sqlalchemy.engine.base.Engine


def test_add_new_record_works():
    """
    Test add_new_record() function adds record to database and returns result
    """
    actual = add_new_record(13,456,"panel_name","panel_version","GMS",23,"r742","transcript","genome_build","bed_file")
    assert type(actual) == sqlalchemy.engine.row.Row


def test_browse_records_no_id():
    """
    Test browse_records() function with no patient ID
    """
    actual = browse_records()
    assert type(actual) == tuple # returns record as table


def test_browse_records_with_id_and_tables(monkeypatch):
    """
    Test browse_records() function with no patient ID
    """
    monkeypatch.setattr('builtins.input', lambda _: "Y") # Choose to view searches information for patient
    actual = browse_records("Patient 1")
    assert type(actual) == tuple # returns record as table


def test_browse_records_with_id_only(monkeypatch):
    """
    Test browse_records() function with no patient ID
    """
    monkeypatch.setattr('builtins.input', lambda _: "N") # Choose not to view searches information for patient
    actual = browse_records("Patient 1")
    assert type(actual) == pandas.core.frame.DataFrame # returns record as pandas dataframe


def test_browse_records_wrong_id():
    """
    Test browse_records() function with no patient ID
    """
    actual = browse_records(2356678)
    expected = "This patient ID does not exist in the SQL database"
    assert actual == expected


def test_download_records(monkeypatch):
    """
    Test download_record() function downloads SQL record as CSV files
    """
    monkeypatch.setattr('builtins.input', lambda _: "Y") # Choose to view searches information for patient
    result = browse_records("Patient 1")  # Get tables from database
    patients_df = result[0]  # Store patients table info
    searches_df = result[1]  # Store search table info
    actual = download_records(patients_df,searches_df,file_name = 'test')
    expected = "[A-Za-z0-9+]_test_patients.csv"
    assert re.search(expected, actual) is not None

