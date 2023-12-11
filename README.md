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
    ├── compose.yaml
    ├── Dockerfile
    ├── installation.md
    ├── LICENCE
    ├── README.md
    ├── requirements.txt
    └── UserGuide.md

Installation
------------

Please see [installation instructions](https://github.com/isabelrem/2023-Software-Development-Assessment/tree/dev/installation.md)

Usage
-----

Please see [user guide](https://github.com/isabelrem/2023-Software-Development-Assessment/tree/dev/UserGuide.md) 
and [readthedocs manual](https://manchester.readthedocs.io/en/dev/)

Testing
-------
To run tests make sure you are in the root directory before typing the following into the terminal

    pytest

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
