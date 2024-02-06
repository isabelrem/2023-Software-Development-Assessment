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
docker exec -it panelsearch bash -c "python main.py"

docker cp panelsearch:/app/panelsearch_downloads .
docker cp panelsearch:/app/PanelSearch/panel_search.log ./PanelSearch
docker cp panelsearch:/app/bed_files .
docker cp panelsearch:/app/PanelSearch/bed_files .



