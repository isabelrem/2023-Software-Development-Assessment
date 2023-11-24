Docker
=====

A Docker Container is available for this app. This still needs to be refined for full functionality with MySQL.



Requirements
-----------

Docker Desktop 4.21.1  or greater is required. Please download from: https://docs.docker.com/get-docker/



How the Docker Image was built
------------------------------

The Docker Image was built using the docker init method::

  docker init


Python v3.1.2 was not compatible with Docker and some versions were not compatible with the requirements.txt file. Therefore Python v3.10 was used.



How to run the Docker container
-----------------------------

Ensure you are in the root directory (2023-Software-Development-Assessment).

Next, build the Docker image::

  docker build -t panelsearch .


Then, run the container with an interactive option and pseudo-terminal::

  docker run -i -t panelsearch


References
-----------
https://docs.docker.com/guides/walkthroughs/containerize-your-app/#:~:text=Containerize%20your%20application%201%20Step%201%3A%20Run%20the,4%20Step%204%3A%20Update%20the%20Docker%20assets%20

https://www.docker.com/blog/how-to-dockerize-your-python-applications/
