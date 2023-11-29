General Usage
-------------

To run please type this code into the command line::

    run main.py


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

    Generate BED file? (y/n)
    > y

This will output a temporary HTML page where you can copy and paste the BED file.
This BED file will be deleted after downloaded.

Finally, it will ask whether you would like to save your results.

Docker
------
Build the docker image
    
    docker build -t panelsearch .

Then, run the container with an interactive option and pseudo-terminal:
    
    docker run -i -t panelsearch
