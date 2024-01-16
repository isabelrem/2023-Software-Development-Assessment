
General Usage (for manual non-Docker use; not recommended)
=============

Please see `Recommended usage: Running PanelSearch in a Docker container`_.

*WARNING: If the user does not want to run their SQL database inside a docker container, please ask Isabel to turn on the cloud-based SQL database before attempting to run code. Alternatively, use MySQL Workbench to manually create a database and modify the code to run locally.*

If the user wishes to run PanelSearch outside of a docker container, the user must install all requirements from requirements.txt locally.

To run PanelSearch, the user should type this code into the command line::

    cd PanelSearch
    python main.py


When prompted choose option 1 for the GRCh37 reference genome build or
option 2 for the GRCh38::

    Which genome build would you like to use? Enter 1 for GRCh37. Enter 2 for GRCh38.
    > 1

When prompted, choose option 1 if you know the R-code or option 2 if you would like to
search by disease name using keywords.

R-code example::

    If you would like to search by R-code, enter 1. If you would like to enter a disease description, enter 2.
    > 1
    Enter your search term:
    > R128

Genetic disease keyword example::

    If you would like to search by R-code, enter 1. If you would like to enter a disease description, enter 2.
    > 2
    Enter your search term:
    > Brugada

When prompted choose whether to generate a BED file::

    Generate BED file? (Y/N)
    > Y

    For exon coordinates on transcript, press \'1\'. For genomic coordinates, press \'2\'.
    > 1


A bed_files folder will be created and your BED file can be found here.

Finally, it will ask whether you would like to save your results::

    Would you like to save this search against a patient ID? (Y/N)
    > Y

    What patient ID would you like to save this search against?
    > Example123

    Your search was saved

    Thank you for using PanelSearch. Goodbye.

Once you have finished remember to deactivate the conda environment::

    conda deactivate
