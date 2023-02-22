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