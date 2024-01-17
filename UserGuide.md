Recommended usage: Running PanelSearch in a Docker container
========
*WARNING: Please ask Isabel to turn on the cloud-based SQL database before attempting to run code. Alternatively, use MySQL Workbench to manually create a database and modify the code to run locally.*

*WARNING: BED files will save within Docker container and database only. BED files will not save locally.*

Users should git clone the repository to their local machine, and navigate into the top level of the repository (2023-Software-Development-Assessment/)

Setting up using the setup.sh script
-----
To setup the app and to run it for the first time, users should run the following code in the top level of the repository:

    ./setup.sh

This will initiate the setup.sh script. Users will be given the choice as to whether they want to set the app up with a dockerised SQL database, or whether they want to instead connect to a cloud database. If the user chooses to use the app with a dockerised SQL database, the setup scripts will create the database container and the database within. With both choices, a docker container for the app will be created and run.

After the app has been setup, to rerun the app users should run the following code in the top level of the repository:

    ./rerun.sh

This will start the necessary docker containers, and reconnect to them.

General Usage
-----
Once the app had begun running, there are several points at which the user is prompted for input. 

When prompted for input type, choose option 1 if you know the R-code or option 2 if you would like to
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

When prompted for genome build, choose option 1 for the GRCh37 reference genome build or
option 2 for the GRCh38::

    Which genome build would you like to use? Enter 1 for GRCh37. Enter 2 for GRCh38.
    > 1

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

Alternative Usage
========
The above is our recommended way to run the app for the smoothest user experience. However, users may install and run the app manually if they wish.

Alternative setups
-------
Unlike the setup and rerun scripts, manually building or running the app will not include automated installation of all required programs. Users should expect to have to troubleshoot errors due to missing requirements.  

Manual Docker PanelSearch setup
--------
These steps can also be found in docker_setup.sh, and involve creating the SQL database and PanelSearch app within Docker containers. Users must already have installed docker and mysql for these commands to work. 

To create the SQL database within a docker container, a network for the two containers to connect via, and a volume for data persistence. If the user wishes to connect to the cloud SQL database instead of a local docker SQL database, **omit this step**.
    
    # create docker network for containers to connect via 
    docker network create panelsearch-network
    echo "panelsearch-network created"
    
    # create docker volume for sql data to be stored on
    docker volume create panelsearch-volume
    echo "panelsearch-volume created"
    
    # create mysql server in the panelsearch-database container
    docker run --name panelsearch-database\
                 --network panelsearch-network \
                --volume panelsearch-volume \
                -e MYSQL_ROOT_PASSWORD=password \
              -d mysql:8
    echo "panelsearch-database container created"
    
    # start mysql 
    #echo "mySQL running"
    sudo service mysql start
    sudo chmod -R 755 /var/run/mysqld
    
    # create panelsearch database and tables on the mysql server
    
    # Set the maximum number of attempts
    max_attempts=100
    
    # Set a counter for the number of attempts
    attempt_num=1
    
    # Set a flag to indicate whether the command was successful
    success=false
    
    # Loop until the command is successful or the maximum number of attempts is reached
    while [ $success = false ] && [ $attempt_num -le $max_attempts ]; do
      # Execute the command
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
    
      # Check the exit code of the command
      if [ $? -eq 0 ]; then
        # The command was successful
        success=true
      else
        # The command was not successful
        echo "Attempt $attempt_num failed. Trying again..."
        sleep 5
        # Increment the attempt counter
        attempt_num=$(( attempt_num + 1 ))
      fi
    done
    
    # Check if the command was successful
    if [ $success = true ]; then
      # The command was successful
      echo "The command was successful after $attempt_num attempts."
    else
      # The command was not successful
      echo "The command failed after $max_attempts attempts."
      exit "Setup aborted. Please try again"
    fi
    
    
    
    echo "panelsearch database created"
    echo "database tables 'searches' and 'patients' created"
    
    # make sure user has docker permissions
    #sudo groupadd docker
    #sudo usermod -aG docker ${USER}
    #newgrp docker
    #echo "User permissions for docker enabled"
    
    sudo chmod 777 PanelSearch/panel_search.log
    echo "permissions enabled"

To build the docker image:
    
    # build the app docker container using the Dockerfile in the repo
    docker buildx build -t panelsearch .
    echo "panelsearch app container created"

To run the docker container for the first time **when using a docker SQL database**:
    
    # run the docker container for the first time
    echo "running panelsearch app... "
    docker run -it --name panelsearch --volume panelsearch-volume \
    --network panelsearch-network panelsearch

To run the docker container for the first time **when using a cloud SQL database**:
    
    # run the docker container for the first time
    echo "running panelsearch app... "
    docker run -it --name panelsearch panelsearch

To run the docker container subsequently **when using either SQL database**:

    docker exec -it panelsearch bash -c "python PanelSearch/main.py"

Manual PanelSearch setup and usage
-------
If the user wishes to run PanelSearch outside of a docker container, the user must install all requirements from requirements.txt locally.

To run PanelSearch, the user should type this code into the command line:

    cd PanelSearch
    python main.py
    
Troubleshooting
-------
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
    
Testing
-------
To run tests make sure you are in the root directory before typing the following into the terminal::

    pytest -vv

You should see::
    
    ================================================================== test session starts ===================================================================
    platform win32 -- Python 3.10.5, pytest-7.4.3, pluggy-1.3.0 -- C:\Users\jessica\AppData\Local\Programs\Python\Python310\python.exe
    cachedir: .pytest_cache
    rootdir: C:\Users\jessica\2023-Software-Development-Assessment
    collected 24 items
    
    Tests/test_PanelApp_API_Request.py::test_request_data PASSED                                                                                        [  4%]
    Tests/test_PanelApp_API_Request.py::test_pk_search PASSED                                                                                           [  8%]
    Tests/test_PanelApp_API_Request.py::test_r_search_works PASSED                                                                                      [ 12%]
    Tests/test_PanelApp_API_Request.py::test_r_search_fails PASSED                                                                                      [ 16%]
    Tests/test_PanelApp_Request_Parse.py::test_panelapp_search_parse_works PASSED                                                                       [ 20%]
    Tests/test_PanelApp_Request_Parse.py::test_panelapp_search_parse_fails PASSED                                                                       [ 25%]
    Tests/test_VV_API_Request.py::test_genome_build_convert_GRch37 PASSED                                                                               [ 29%] 
    Tests/test_VV_API_Request.py::test_genome_build_convert_fails PASSED                                                                                [ 33%] 
    Tests/test_VV_API_Request.py::test_request_data_works PASSED                                                                                        [ 37%]
    Tests/test_VV_API_Request.py::test_gene_to_transcripts_works PASSED                                                                                 [ 41%]
    Tests/test_VV_Request_Parse.py::test_vv_request_parse PASSED                                                                                        [ 45%]
    Tests/test_functional.py::test_main_works PASSED                                                                                                    [ 50%]
    Tests/test_generate_bed.py::test_parse_panel_data PASSED                                                                                            [ 54%]
    Tests/test_generate_bed.py::test_write_bed_file_works PASSED                                                                                        [ 58%]
    Tests/test_generate_bed.py::test_write_bed_file_no_filename PASSED                                                                                  [ 62%]
    Tests/test_generate_bed.py::test_write_bed_file_no_beds PASSED                                                                                      [ 66%] 
    Tests/test_main.py::test_get_genome_build_works PASSED                                                                                              [ 70%] 
    Tests/test_main.py::test_get_genome_build_errors PASSED                                                                                             [ 75%] 
    Tests/test_main.py::test_get_input_string_type_works PASSED                                                                                         [ 79%] 
    Tests/test_main.py::test_get_input_string_type_errors PASSED                                                                                        [ 83%]
    Tests/test_main.py::test_get_input_string PASSED                                                                                                    [ 87%] 
    Tests/test_main.py::test_create_bed_filename PASSED                                                                                                 [ 91%] 
    Tests/test_select_disease.py::test_find_match_works PASSED                                                                                          [ 95%]
    Tests/test_select_disease.py::test_find_match_errors PASSED                                                                                         [100%]
    
    ================================================================== 24 passed in 57.21s ===================================================================


References
-----------
https://docs.docker.com/guides/walkthroughs/containerize-your-app/#:~:text=Containerize%20your%20application%201%20Step%201%3A%20Run%20the,4%20Step%204%3A%20Update%20the%20Docker%20assets%20

https://www.docker.com/blog/how-to-dockerize-your-python-applications/

