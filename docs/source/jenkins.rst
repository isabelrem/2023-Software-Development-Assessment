Jenkins Continuous Integration/Development
==========================================

Jenkins is a tool that automates building, testing, and deploying. For more information please visit: https://www.jenkins.io/doc/book/pipeline/jenkinsfile/

Here is a useful Jenkins tutorial series: https://www.youtube.com/watch?v=pMO26j2OUME&list=PLy7NrYWoggjw_LIiDK1LXdNN82uYuuuiC

Command-line set-up
------------------
Instructions::
  
  # Install Jenkins
  docker pull jenkins/jenkins
  
  # Create a volume
  docker volume create jenkins-shared-space

  # Run Jenkins
  docker run -d -u root --name jenkins-docker -p 8080:8080 -p 50000:50000 --restart=on-failure -v jenkins-data:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -v jenkins-shared-space:/var/shared-data jenkins/jenkins:lts-jdk11 
  
  # Get admin password for Jenkins
  docker ps  # Note down Container ID
  docker logs <Container ID>  # Note down Password
  
  # Enter the container by its name and access its bash shell
  docker exec -it jenkins-docker /bin/bash 
  
  # Run the following commands to setup docker within the container
  apt update
  apt install -y docker.io
  apt install python3.11-venv
  apt install pip
  apt install python3-pytest
  apt install less
  apt install docker
  
  # Alternative way of finding password
  cd /var/jenkins_home/secrets
  less initialAdminPassword
  
  # Run the following command to setup a safe workspace for your Jenkins projects
  git config --global --add safe.directory "*"


GUI set-up
----------
Head to http://localhost:8080/ in your browser.

Install recommended plugins.

Enter the admin password and create a user.

Head to *Dashboard --> Manage Jenkins --> Plugins --> Available plugins*
 
You will need to install these extra plugins:

* Git server
* GitHub Integration
* Docker
* Docker pipeline
* Docker API
* Pyenv Pipeline
* docker-build-step

Go to the *Dashboard* and create a new item.

Select an appropriate pipeline name e.g. my-pipeline.

Select *Multibranch Pipeline* and click *OK*.

Under *Dashboard --> <Pipeline name> --> Configure --> Branch Sources* add the GitHub repository https://github.com/isabelrem/2023-Software-Development-Assessment and add the correct credentials (see below for instruction on how to create credentials).

Under *Dashboard --> <Pipeline name> --> Configure --> Branch Sources --> Behaviours --> Discover Branches* change the strategy to *Only branches that are also filed as PRs*.

Under *Dashboard --> Pipeline --> Configure --> Scan Repository Triggers* tick the option and choose the appropriate interval. This will run the process automatically.

Under *Dashboard --> Pipeline* click *Scan Respository Now* Now to run the process manually.


Create credentials
-----------------

Under *Dashboard --> Manage Jenkins --> Credentials* click on the appropriate user and domain e.g. *System --> Global*.

Click *Add Credentials* and enter your GitHub username and password.

Leave the scope as Global and click *Create*.

