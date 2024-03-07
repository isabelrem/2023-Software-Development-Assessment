#!/bin/bash

# Welcome message

echo "Welcome to PanelSearch!" 

# Check whether docker containers already exist
# If not, perform setup.

database=$(docker ps -a | grep -o "panelsearch-database")
app=$(docker ps -a | grep -o " panelsearch ") # need spaces around panelsearch to exclude panelsearch-database and panelsearch-volume etc. 

database_present="panelsearch-database"
app_present=" panelsearch "

if [[ "$database" == "$database_present" ]]
then
    echo "Database already present! Checking for app container..."

    if [[ "$app" == "$app_present" ]]
    then
        echo "App container already present! Proceeding..."

        # make sure the docker container for the app + db are running
        docker start panelsearch
        docker start panelsearch-database

        # containers are present and running - run the app
        docker exec -it panelsearch bash -c "python main.py"

        # download the files created in the container
        docker cp panelsearch:/app/panelsearch_downloads .
        docker cp panelsearch:/app/panel_search.log ./PanelSearch
        docker cp panelsearch:/app//bed_files .
        
    else
        echo "Database is present but App container is not. Running setup..."
        echo "Proceeding with docker set up..."
        # sets up containers and runs app
        ./docker_setup.sh
    fi
else
    echo "Database not present. Running setup..."
    echo "Proceeding with docker set up..."
    # sets up containers and runs app
    ./docker_setup.sh
fi



