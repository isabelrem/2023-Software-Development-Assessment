#!/bin/bash
#rm panelsearch_downloads/*
sudo aa-remove-unknown
docker stop panelsearch-database
docker stop panelsearch
docker rm panelsearch-database
docker rm panelsearch
docker image rm panelsearch
docker network rm panelsearch-network
docker volume rm panelsearch-volume
#yes | docker system prune -a 
./setup.sh