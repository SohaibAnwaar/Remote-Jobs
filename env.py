from typing import Optional
from pydantic import BaseSettings

# This is a pydantic model for the enviroment variables


class Settings(BaseSettings):
    
    # Database
    database_hostname: str = 'localhost'
    database_password: str = 'postgres'
    database_name: str = 'scraper'
    database_username: str = 'postgres'
    database_port: str = '5432'
    
    # Kafka
    kafka_host: str = 'localhost'
    kafka_port: str = '9092'
    kafka_topic: str = 'scrapper'
    kafka_group_id: str = 'scrapper'

    # Logging
    log_level: str = 'INFO'
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_date_format: str = '%Y-%m-%d %H:%M:%S'
    main_log_path: str = 'logs/main.log'
    db_log_path: str = 'logs/db.log'
    scrapper_log_path: str = 'logs/scraper/'

    # Scrappers
    simutanious_scrappers: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
