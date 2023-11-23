# State the base image
FROM python:3.1.2

# Set the working directory to /app
WORKDIR /app

# Mount the current host directory to the container's /app directory
VOLUME /app

# Create logging directory
RUN mkdir /logs

# Update apt-get
RUN apt-get update

# Install git
RUN apt-get -y install git

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Define the entrypoint as an empty command
# This allows for flexibility in specifying the command when running the container.
# You can override this by providing a command when running the container with 'docker run'.
ENTRYPOINT []

# Start the container by running a specific Python script. The "tail", "-f", "/dev/null" command allows the container
# to keep running in detached mode untill it it killed manually
CMD ["python", "~/panelsearch/main.py", "tail", "-f", "/dev/null"]
