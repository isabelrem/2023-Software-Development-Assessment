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
    

Docker
------
        
    docker network create panelsearch-network
    
    docker volume create panelsearch-volume

    docker run --name panelsearch-database\
                 --network panelsearch-network\
                --volume panelsearch-volume\
                -e MYSQL_ROOT_PASSWORD=password\
              -d mysql:8

    docker exec panelsearch-database mysql -uroot -ppassword -e "CREATE DATABASE IF NOT EXISTS panelsearch;"

    docker exec panelsearch-database mysql -uroot -ppassword -e \
    "CREATE DATABASE IF NOT EXISTS panelsearch;\
     CREATE TABLE IF NOT EXISTS panelsearch.patients( \
                    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,\
                    patient_id varchar(50),\
                    search_id int);\
     CREATE TABLE IF NOT EXISTS panelsearch.searches( \
                    id int KEY AUTO_INCREMENT, \
                    panel_id int, \
                    panel_name varchar(500),\
                    panel_version varchar(50),\
                    GMS varchar(50),\
                    gene_number int,\
                    r_code varchar(5),\
                    transcript varchar(50),\
                    genome_build varchar(50),\
                    bed_file varchar(50),\
                    UNIQUE (panel_id, panel_name, panel_version, GMS, gene_number, r_code, \
                         transcript, genome_build, bed_file)\
                    );"


------
Build the docker image
    
    docker build -t panelsearch .

Then, run the container with an interactive option and pseudo-terminal:
    
    docker run -it --name panelsearch --volume panelsearch-volume \
    --network panelsearch-network panelsearch

After having run the app once, the container should exist the interactive terminal. To reenter the interactive terminal and use the app again, enter into the command line:

    docker exec -it panelsearch bash -c "python PanelSearch/main.py"

Troubleshooting error messsage: 'docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock:' 

    sudo groupadd docker

    sudo usermod -aG docker $USER
    
    newgrp docker

Troubleshooting error message: 'ERROR: Cannot connect to the Docker daemon at unix://?var/run/docker.sock. Is the docker daemon running?
    
    sudo systemct1 start docker


Troubleshooting error message: 'ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)'
    * suggested tutorial: https://phoenixnap.com/kb/mysql-server-through-socket-var-run-mysqld-mysqld-sock-2
    
    sudo apt install mysql-server
    sudo service mysql start
    
Docker - all code in one block for copying purposes
      
        
    docker network create panelsearch-network
    
    docker volume create panelsearch-volume

    docker run --name panelsearch-database\
                 --network panelsearch-network\
                --volume panelsearch-volume\
                -e MYSQL_ROOT_PASSWORD=password\
              -d mysql:8

    docker exec panelsearch-database mysql -uroot -ppassword -e "CREATE DATABASE IF NOT EXISTS panelsearch;"

    docker exec panelsearch-database mysql -uroot -ppassword -e \
    "CREATE DATABASE IF NOT EXISTS panelsearch;\
     CREATE TABLE IF NOT EXISTS panelsearch.patients( \
                    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,\
                    patient_id varchar(50),\
                    search_id int);\
     CREATE TABLE IF NOT EXISTS panelsearch.searches( \
                    id int KEY AUTO_INCREMENT, \
                    panel_id int, \
                    panel_name varchar(500),\
                    panel_version varchar(50),\
                    GMS varchar(50),\
                    gene_number int,\
                    r_code varchar(5),\
                    transcript varchar(50),\
                    genome_build varchar(50),\
                    bed_file varchar(50),\
                    UNIQUE (panel_id, panel_name, panel_version, GMS, gene_number, r_code, \
                         transcript, genome_build, bed_file)\
                    );"
                    
    docker build -t panelsearch .
    
    docker run -it --name panelsearch --volume panelsearch-volume \
    --network panelsearch-network panelsearch


