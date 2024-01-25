PanelSearch
===========

Description
-----------

A tool to manage gene panels for NHS National Genomic Testing Directory tests in the laboratory.
Allows user to search for gene panels and outputs BED file.
Search history can be saved to a database and retrieved at a later date.
Release 1.0 of PanelSearch currently uses v5.1 of the National Genomic Testing Directory.

Dependencies
------------

Python 3.10 or greater is required to run this app. This app connects to the PanelApp API so requires an internet connection. Also, a MySQL database is created through this app so we recommend installing MySQLWorkBench https://www.mysql.com/products/workbench/ .

Features
--------

- Returns gene panel information
- Returns BED file
- Saves gene panel information

Directory Tree
-------------
    .
    ├── PanelSearch.egg-info
    │   ├── PKG-INFO
    │   ├── SOURCES.txt
    │   ├── dependency_links.txt
    │   ├── requires.txt
    │   └──  top_level.txt
    ├── PanelSearch
    │   ├── __init__.py
    │   ├── API_to_SQL.py
    │   ├── generate_bed.py
    │   ├── main.py
    │   ├── PanelApp_API_Request
    │   ├── PanelApp_Request_Parse.py
    │   ├── select_disease.py
    │   ├── SQL_functions.py
    │   ├── VV_API_Request.py
    │   └── VV_Request_Parse.py
    ├── docs/source
    │   ├── api.rst
    │   ├── conf.py
    │   ├── docker.rst
    │   ├── index.rst
    │   ├── installation.rst
    │   ├── jenkins.rst
    │   ├── sql.rst
    │   ├── sql_schema.png
    │   └──  usage.rst
    ├── sql_fun
    │   ├── panelsearch_db.sql
    │   └── sql_schema.png
    ├── Tests
    │   ├── __init__.py
    │   ├── test_generate_bed.py
    │   ├── test_main.py
    │   ├── test_PanelApp_API_Request.py
    │   ├── test_PanelApp_Request_Parse.py
    │   ├── test_select_disease.py
    │   ├── test_VV_API_Request.py
    │   └── test_VV_Request_Parse.py
    ├── .dockerignore
    ├── .gitignore
    ├── .readthedocs.yaml
    ├── Dockerfile
    ├── Jenkinsfile
    ├── LICENCE
    ├── README.md
    ├── UserGuide.md
    ├── compose.yaml
    ├── docker_setup.sh
    ├── environment.yaml
    ├── installation.md
    ├── pyproject.toml
    ├── requirements.txt
    ├── rerun.sh
    ├── setup.sh
    └── var


Installation
------------

Please see [installation instructions](https://github.com/isabelrem/2023-Software-Development-Assessment/tree/dev/installation.md)

Usage
-----

Please see [user guide](https://github.com/isabelrem/2023-Software-Development-Assessment/tree/dev/UserGuide.md) 
and [readthedocs manual](https://manchester.readthedocs.io/en/dev/)

Testing
-------
To run tests make sure you are in the root directory before typing the following into the terminal::

    pytest -vv

You should see::
    
    ============================================================================================= test session starts =============================================================================================
    platform win32 -- Python 3.10.5, pytest-7.4.3, pluggy-1.3.0 -- C:\Users\AppData\Local\Programs\Python\Python310\python.exe
    cachedir: .pytest_cache
    rootdir: C:\Users\2023-Software-Development-Assessment
    collected 35 items
    
    Tests/test_API_to_SQL_cloud.py::test_PK_Parse_Data_to_SQL_cloud_works PASSED                                                                                                                             [  2%]
    Tests/test_API_to_SQL_cloud.py::test_PK_Parse_Data_to_SQL_cloud_type_errors PASSED                                                                                                                       [  5%] 
    Tests/test_API_to_SQL_cloud.py::test_PK_Parse_Data_to_SQL_cloud_value_errors PASSED                                                                                                                      [  8%] 
    Tests/test_PanelApp_API_Request.py::test_request_data PASSED                                                                                                                                             [ 11%]
    Tests/test_PanelApp_API_Request.py::test_pk_search PASSED                                                                                                                                                [ 14%]
    Tests/test_PanelApp_API_Request.py::test_r_search_works PASSED                                                                                                                                           [ 17%]
    Tests/test_PanelApp_API_Request.py::test_r_search_fails PASSED                                                                                                                                           [ 20%]
    Tests/test_PanelApp_Request_Parse.py::test_panelapp_search_parse_works PASSED                                                                                                                            [ 22%]
    Tests/test_PanelApp_Request_Parse.py::test_panelapp_search_parse_fails PASSED                                                                                                                            [ 25%]
    Tests/test_SQL_Cloud_Functions.py::test_docker_or_cloud_works PASSED                                                                                                                                     [ 28%]
    Tests/test_SQL_Cloud_Functions.py::test_connect_cloud_db_works PASSED                                                                                                                                    [ 31%]
    Tests/test_SQL_Cloud_Functions.py::test_add_new_cloud_record_works PASSED                                                                                                                                [ 34%]
    Tests/test_SQL_Cloud_Functions.py::test_browse_cloud_records_no_id PASSED                                                                                                                                [ 37%]
    Tests/test_SQL_Cloud_Functions.py::test_browse_cloud_records_with_id_and_tables PASSED                                                                                                                   [ 40%]
    Tests/test_SQL_Cloud_Functions.py::test_browse_cloud_records_with_id_only PASSED                                                                                                                         [ 42%]
    Tests/test_SQL_Cloud_Functions.py::test_browse_cloud_records_wrong_id PASSED                                                                                                                             [ 45%]
    Tests/test_SQL_Cloud_Functions.py::test_download_records PASSED                                                                                                                                          [ 48%]
    Tests/test_VV_API_Request.py::test_genome_build_convert_GRch37 PASSED                                                                                                                                    [ 51%] 
    Tests/test_VV_API_Request.py::test_genome_build_convert_fails PASSED                                                                                                                                     [ 54%] 
    Tests/test_VV_API_Request.py::test_request_data_works PASSED                                                                                                                                             [ 57%]
    Tests/test_VV_API_Request.py::test_gene_to_transcripts_works PASSED                                                                                                                                      [ 60%]
    Tests/test_VV_Request_Parse.py::test_vv_request_parse PASSED                                                                                                                                             [ 62%]
    Tests/test_functional.py::test_main_works PASSED                                                                                                                                                         [ 65%]
    Tests/test_generate_bed.py::test_parse_panel_data PASSED                                                                                                                                                 [ 68%]
    Tests/test_generate_bed.py::test_write_bed_file_works PASSED                                                                                                                                             [ 71%]
    Tests/test_generate_bed.py::test_write_bed_file_no_filename PASSED                                                                                                                                       [ 74%]
    Tests/test_generate_bed.py::test_write_bed_file_no_beds PASSED                                                                                                                                           [ 77%] 
    Tests/test_main.py::test_get_genome_build_works PASSED                                                                                                                                                   [ 80%] 
    Tests/test_main.py::test_get_genome_build_errors PASSED                                                                                                                                                  [ 82%] 
    Tests/test_main.py::test_get_input_string_type_works PASSED                                                                                                                                              [ 85%]
    Tests/test_main.py::test_get_input_string_type_errors PASSED                                                                                                                                             [ 88%] 
    Tests/test_main.py::test_get_input_string PASSED                                                                                                                                                         [ 91%] 
    Tests/test_main.py::test_create_bed_filename PASSED                                                                                                                                                      [ 94%] 
    Tests/test_select_disease.py::test_find_match_works PASSED                                                                                                                                               [ 97%]
    Tests/test_select_disease.py::test_find_match_errors PASSED                                                                                                                                              [100%]
    
    ======================================================================================= 35 passed in 164.41s (0:02:44) ========================================================================================
    
Contribute
----------

- Issue Tracker: https://github.com/isabelrem/2023-Software-Development-Assessment/issues
- Source Code: https://github.com/isabelrem/2023-Software-Development-Assessment
- Trello: https://trello.com/b/gWEfG504/team-3-mie

Support
-------

If you are having issues, please let us know.

License
-------

This project is [currently licensed](https://github.com/isabelrem/2023-Software-Development-Assessment/tree/dev/LICENCE) under the MIT licence.

Authors
-------
Isabel, Tom, Egle, and Jess
