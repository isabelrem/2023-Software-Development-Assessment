"""
Test functions from SQL_Cloud_Functions.py
"""

# import functions
from PanelSearch.SQL_Cloud_Functions import *
import sqlalchemy
import pandas
import re

def test_docker_or_cloud_works():
    """
    Test docker_or_cloud() function creates connection string
    """
    actual = docker_or_cloud()
    expected = 'mysql+pymysql://panelsearch_user:panelsearch_password@35.197.209.133:3306/panelsearch'
    assert actual == expected


def test_connect_cloud_db_works():
    """
    Test connect_cloud_db() function creates engine
    """
    actual = connect_cloud_db()
    assert type(actual) == sqlalchemy.engine.base.Engine


def test_add_new_cloud_record_works():
    """
    Test add_new_cloud_record() function adds record to database and returns result
    """
    actual = add_new_cloud_record(13,456,"panel_name","panel_version","GMS",23,"r742","transcript","genome_build","bed_file")
    assert type(actual) == sqlalchemy.engine.row.Row


def test_browse_cloud_records_no_id():
    """
    Test browse_cloud_records() function with no patient ID
    """
    actual = browse_cloud_records()
    assert type(actual) == tuple # returns record as table


def test_browse_cloud_records_with_id_and_tables(monkeypatch):
    """
    Test browse_cloud_records() function with no patient ID
    """
    monkeypatch.setattr('builtins.input', lambda _: "Y") # Choose to view searches information for patient
    actual = browse_cloud_records("Patient 1")
    assert type(actual) == tuple # returns record as table


def test_browse_cloud_records_with_id_only(monkeypatch):
    """
    Test browse_cloud_records() function with no patient ID
    """
    monkeypatch.setattr('builtins.input', lambda _: "N") # Choose not to view searches information for patient
    actual = browse_cloud_records("Patient 1")
    assert type(actual) == pandas.core.frame.DataFrame # returns record as pandas dataframe


def test_browse_cloud_records_wrong_id():
    """
    Test browse_cloud_records() function with no patient ID
    """
    actual = browse_cloud_records(2356678)
    expected = "This patient ID does not exist in the SQL database"
    assert actual == expected


def test_download_records():
    """
    Test download_record() function downloads SQL record as CSV files
    """
    result = browse_cloud_records("Patient 1")  # Get tables from database
    patients_df = result[0]  # Store patients table info
    searches_df = result[1]  # Store search table info
    actual = download_records(patients_df,searches_df,file_name = 'test')
    expected = "[A-Za-z0-9+]_test_patients.csv"
    assert re.search(expected, actual) is not None

