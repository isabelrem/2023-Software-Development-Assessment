#!/bin/bash

# install docker if not present

# check if any docker is installed
# if not, install docker.io and docker-buildx
# REQUIRED_PKG="docker*"
# PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
# echo Checking for $REQUIRED_PKG: $PKG_OK
# if [ "" = "$PKG_OK" ]; then
#   echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
#   sudo apt-get --yes install docker.io
#   sudo apt-get --yes install docker-buildx
# fi

if [ -x "$(command -v docker)" ]; then
  echo "A version of docker is already installed"
else
  echo "No docker installed. Setting up docker..."
  sudo apt-get --yes install docker.io
  sudo apt-get --yes install docker-buildx
fi


# install docker buildx if not present
# REQUIRED_PKG="docker-buildx"
# PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
# echo Checking for $REQUIRED_PKG: $PKG_OK
# if [ "" = "$PKG_OK" ]; then
#   echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
#   sudo apt-get --yes install $REQUIRED_PKG
# fi

# make sure user has docker permissions # uncomment for next fresh install
#sudo groupadd docker 
#sudo usermod -aG docker ${USER}
#newgrp docker
#echo "User permissions for docker enabled"

#sleep 20

sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "$HOME/.docker" -R

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
                bed_file_config varchar(50),\
                bed_file longtext,\
                UNIQUE (panel_id, panel_name, panel_version, GMS, gene_number, r_code, \
                     transcript, genome_build, bed_file_config)\
                );" 2>/dev/null
  # need a field for bed file combination, (exon or genome, padding), bc otherwsie can only save one bed file per gene test
  # will have to add to cloud too
  # Check the exit code of the command
  if [ $? -eq 0 ]; then
    # The command was successful
    success=true
  else
    # The command was not successful
    echo "Connecting, please wait..."
    sleep 5
    # Increment the attempt counter
    attempt_num=$(( attempt_num + 1 ))
  fi
done

# Check if the command was successful
if [ $success = true ]; then
  # The command was successful
  echo "Successfully connected to docker SQL database."
else
  # The command was not successful
  echo "Connection failed after $max_attempts attempts."
  exit "Setup aborted. Please try again"
fi



echo "panelsearch database created"
echo "database tables 'searches' and 'patients' created"

# make sure user has docker permissions
#sudo groupadd docker
#sudo usermod -aG docker ${USER}
#newgrp docker
#echo "User permissions for docker enabled"

sudo chmod -R 777 .
sudo chmod 777 PanelSearch/panel_search.log
echo "permissions enabled"

# build the app docker container using the Dockerfile in the repo
docker buildx build -t panelsearch .
echo "panelsearch app container created"

# run the docker container for the first time
echo "running panelsearch app... "
docker run -it --name panelsearch --volume panelsearch-volume \
 --network panelsearch-network panelsearch

