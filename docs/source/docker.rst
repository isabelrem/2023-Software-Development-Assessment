Docker
=====

A Docker Container is available for this app. This still needs to be refined for full functionality with MySQL.



Requirements
-----------

Docker Desktop 4.21.1  or greater is required. Please download from: https://docs.docker.com/get-docker/



How the Docker Image was built
------------------------------

The Docker Image was built using the docker init method::

  docker init


Python v3.1.2 was not compatible with Docker and some versions were not compatible with the requirements.txt file. Therefore Python v3.10 was used.



How to run the Docker container
-----------------------------

Ensure you are in the root directory (2023-Software-Development-Assessment).

Create the Docker Network::

          
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




Next, build the Docker image::

  docker build -t panelsearch .


Then, run the container with an interactive option and pseudo-terminal::

    docker run -it --name panelsearch --volume panelsearch-volume \
    --network panelsearch-network panelsearch

After having run the app once, the container should exist the interactive terminal. To reenter the interactive terminal and use the app agai
n, enter into the command line::
  
    docker exec -it panelsearch bash -c "python PanelSearch/main.py"


Troubleshooting error messsage: 'docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock:' ::
  
    sudo groupadd docker
  
    sudo usermod -aG docker $USER
    
    newgrp docker


Troubleshooting error message: 'ERROR: Cannot connect to the Docker daemon at unix://?var/run/docker.sock. Is the docker daemon running? ::
    
    sudo systemct1 start docker
  

Troubleshooting error message: "ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)" 
    * suggested tutorial: https://phoenixnap.com/kb/mysql-server-through-socket-var-run-mysqld-mysqld-sock-2 

Try ::
    sudo apt install mysql-server
    sudo service mysql start
  

References
-----------
https://docs.docker.com/guides/walkthroughs/containerize-your-app/#:~:text=Containerize%20your%20application%201%20Step%201%3A%20Run%20the,4%20Step%204%3A%20Update%20the%20Docker%20assets%20

https://www.docker.com/blog/how-to-dockerize-your-python-applications/
