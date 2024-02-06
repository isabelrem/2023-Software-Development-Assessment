#!/bin/bash
#rm panelsearch_downloads/*
sudo aa-remove-unknown
docker stop panelsearch-database
docker stop panelsearch
yes | docker system prune -a 
./setup.sh