# Introduction

Idea is to scrap jobs from different Job-Portals and generate remote job list. So that we can search for jobs from different portals at one place.

# Installation

## Create env file
```bash
cp .env.example .env
```

## Install dependencies
```bash
# Install pyenv
curl https://pyenv.run | bash

# Install python 3.9.13
pyenv install 3.9.13

# Create virtualenv
pyenv virtualenv 3.9.13 scraper

# Activate virtualenv
pyenv activate scraper

# Install dependencies
pip install -r requirements.txt

```
Now you have to install docker into your system. You can find the installation guide [here](https://docs.docker.com/engine/install/).

go to `docker` directory and run this command to start the postgres server.
```bash
docker-compose up -d
```
for docker-compose status run this command
```bash
docker-compose ps
```

## Create Database
1. Create the Database name `scraper` in postgres.
2. Run this command to create tables.
```bash
# Create database
python shared_layer/postgres/make_tables.py 
```

## Start the server
```bash
# Start the server
python main.py
```

## Development Environment
if you want to run the server in development mode, then you need to set `ENV` to `dev` in `.env` file.

mention scrapers here you want to run in development mode `scrappers/scrapper/available_scrappers_dev.json`

