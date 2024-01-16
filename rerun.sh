#!/bin/bash

# make sure the docker container for the app is running
docker start panelsearch

# check whether a database container was made during setup
database=$(docker ps -a | grep -o "panelsearch-database")
docker_present="panelsearch-database"
if [[ "$database" == "$docker_present" ]]
then
        # make sure docker container for database is working
        docker start panelsearch-database
        echo "starting app with docker database"
        
else
        echo "starting app with cloud database"
fi

# run the app
docker exec -it panelsearch bash -c "python PanelSearch/main.py"
