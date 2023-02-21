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