#!/bin/bash

echo """
Welcome to PanelSearch! 
If you would like to setup the app with a Docker container SQL database, please enter '1'. If you would like to setup the app with a cloud SQL database, please enter '2'."""

read cloud_or_docker

cloud=2
docker=1


if [ $cloud_or_docker -eq $docker ]
then
        echo "Proceding with docker set up..."
        ./docker_setup.sh
else
        # build the app docker container using the Dockerfile in the repo
        docker buildx build -t panelsearch .
        echo "panelsearch app container created"

        # run the docker container for the first time
        echo "running panelsearch app... "
        docker run -i -t --name panelsearch panelsearch # one panelsearch is naming the container 
        # the other is specifying the image to use
fi



