.. PanelSearch documentation master file, created by
   sphinx-quickstart on Thu Nov  9 14:21:39 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PanelSearch's documentation!
=======================================

.. toctree::
  :maxdepth: 2
  :caption: Contents:

  index  
  installation
  usage
  api
  sql
  docker
  jenkins
  


Description
-----------

A tool to manage gene panels for NHS National Genomic Testing Directory tests in the laboratory.
Allows user to search for gene panels and outputs BED file.
Search history can be saved to a database and retrieved at a later date.
Release 1.0 of PanelSearch currently uses v5.1 of the National Genomic Testing Directory.


Dependencies
------------
Python 3.1.2 or greater is required to run this app. This app connects to the PanelApp API so requires an internet connection. Also, a MySQL database is created through this app so we recommend installing MySQLWorkBench https://www.mysql.com/products/workbench/ .


Features
--------

- Returns gene panel information
- Returns BED file
- Saves gene panel information


Testing
-------
To run tests make sure you are in the root directory before typing the following into the terminal::
    
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

This project is currently licensed under the MIT licence.

Authors
-------

- Tom
- Isabel
- Egle
- Jess

