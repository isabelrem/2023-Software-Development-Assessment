#!/bin/bash

docker stop panelsearch
yes | docker system prune -a 
./setup.sh