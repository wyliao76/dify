# COMP3800-Group20

# Install pyenv

## MacOS
- >brew update
- >brew install pyenv

## Linux/Unix
>curl -fsSL https://pyenv.run | bash

# Setting up python environment (pyenv)

## Install python version 3.12.0 for project
>pyenv install 3.12.0

## Create virtual env
At project root:
>python3 -m venv venv

## Activate python environment
>source venv/bin/activate

## Install python libraries/packages
At project root:
>pip3 install -r requirements-dev.txt

## To leave python environment

>deactivate

# Disable __pycache__
>export PYTHONDONTWRITEBYTECODE=1

# Docker

## Install
Install docker desktop via package manager

### Setup Database
At project root:
>docker compose up -d

### Teardown container
>docker compose down -v

### docker commands
To find container id:
>docker ps

### export / import database
Through docker desktop, open the container and use terminal and run the commands written in: scripts/export.sh / scripts/import.sh

# Install node
Install nvm or node 22 directly: https://nodejs.org/en/download

# install npm packages
At project root:
>npm ci

# create env.local in src folder
>cp env.example /src/.env.local

Roboflow API Key to be obtained through the Roboflow Platform through (Settings -> API Keys -> Private API Key)<br>

If you want to use different database credentials, you will also need to change the credentials in docker-compose.yml before setting up the container

## Run
Activate pyenv:
>source venv/bin/activate<br>

Run server:
>npm run local

# Accessible pages (examples assume hosting on port 8080):

Appointment volume prediction page:
>http://localhost:8080/schedule<br>

Panoramic x-ray annotation page:
>http://localhost:8080/xray<br>

Demographic prediction page:
>http://localhost:8080/predict<br>

Records upload paage:
>http://localhost:8080/upload<br>