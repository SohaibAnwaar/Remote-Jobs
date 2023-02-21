from typing import Optional
from pydantic import BaseSettings

# This is a pydantic model for the enviroment variables


class Settings(BaseSettings):
    database_hostname: str = 'localhost'
    database_password: str = 'postgres'
    database_name: str = 'scrapers'
    database_username: str = 'postgres'
    database_port: str = '5432'
    class Config:
        env_file = ".env"


settings = Settings()
