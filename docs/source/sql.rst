SQL Database
============

The SQL database needs to be created manually and stores information about the search.

One table is called patients and stores the patient ID and search ID.

The other table is called searches and holds the search information generated. This includes the panel ID, panel name, panel version, GMS signed-off status, gene names, R code of panels, MANE select transcripts, genome build, and BED file as a JSON.

.. image:: https://github.com/isabelrem/2023-Software-Development-Assessment/edit/dev/sql_fun/sql_schema.png
  :width: 400
  :alt: SQL schema
