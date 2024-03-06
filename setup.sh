#!/bin/bash

echo "Welcome to PanelSearch!" 

# setup of docker containers for the app and the SQL db

echo "Proceeding with docker set up..."
./docker_setup.sh

# grabs the contents of the directory instead of the directory - prevents system getting grouchy about overwrite?

docker cp panelsearch:/app/panelsearch_downloads .
docker cp panelsearch:/app/PanelSearch/panel_search.log ./PanelSearch
docker cp panelsearch:/app/bed_files .
docker cp panelsearch:/app/PanelSearch/bed_files .


