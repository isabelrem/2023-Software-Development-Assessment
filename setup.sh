#!/bin/bash

# install docker if not present
REQUIRED_PKG="docker.io"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG
fi

# install docker buildx if not present
REQUIRED_PKG="docker-buildx"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG
fi

# make sure user has docker permissions # uncomment for next fresh install
#sudo groupadd docker || true
#sudo usermod -aG docker ${USER}
#newgrp docker
#echo "User permissions for docker enabled"

#sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
#sudo chmod g+rwx "$HOME/.docker" -R

# makes sure docker is running
sudo systemctl start docker
echo "Docker running"

# install mysql-server if not present
REQUIRED_PKG="mysql-server"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG
fi

# create docker network for containers to connect via 
docker network create panelsearch-network
echo "panelsearch-network created"

# create docker volume for sql data to be stored on
docker volume create panelsearch-volume
echo "panelsearch-volume created"

# create mysql server in the panelsearch-database container
docker run --name panelsearch-database\
             --network panelsearch-network\
            --volume panelsearch-volume\
            -e MYSQL_ROOT_PASSWORD=password\
          -d mysql:8
echo "panelsearch-database container created"

# start mysql 
#echo "mySQL running"
sudo service mysql start

# create panelsearch database and tables on the mysql server
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
echo "panelsearch database created"
echo "database tables 'searches' and 'patients' created"

# make sure user has docker permissions
#sudo groupadd docker
#sudo usermod -aG docker ${USER}
#newgrp docker
#echo "User permissions for docker enabled"

# build the app docker container using the Dockerfile in the repo
docker buildx build -t panelsearch .
echo "panelsearch app container created"

# run the docker container for the first time
echo "running panelsearch app... "
docker run -it --name panelsearch --volume panelsearch-volume \
--network panelsearch-network panelsearch
