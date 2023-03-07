from abc import ABCMeta, abstractmethod
from datetime import datetime
import time
from collections import deque

from env import settings
from scrappers.helper import get_title
from shared_layer.kafka.producer import KafkaProducerBridge
from shared_layer.postgres.database import Database
from shared_layer.variables import in_progress



class Scrapper(metaclass=ABCMeta):
    """This is the Parent class for all the scrappers
    every scrapper should be inherit by this scrapper
    to get the ouput. If some of the variables are not
    initilised in child/scrapper class then by defualt
    these variables will be used.

    Features: 
            - Singleton Class = Only 1 object through out the project life
            - Abstract class = Need to implement the speceifc function which are requried e.g (run)
    Args:
            ABC (OBJ): Abstract class object
    """
    _INSTANCE = None
    # Class vars

    def __init__(self) -> None:
        self.db = Database()
        self.date_time_format = "%Y-%m-%d %H:%M:%S"
        self.instance = None
        self.delay = 1380
        self.tags = []
        self.kafka_producer = KafkaProducerBridge()
        self.name = "Main"
        self.page_limit = 4

    def __del__(self):
        """
        """
        pass

    @classmethod
    def singleton(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls.create_singleton_obj(*args, **kwargs)
        return cls._INSTANCE

    @classmethod
    def create_singleton_obj(cls, logger=None):  # by default None
        """Get the singleton scraper Object

        Returns:
        Kimeta : Initialize Scraper object and return object
        """
        return cls(logger)

    @abstractmethod
    def scrap(self):
        """Every scrapper class have run class
        which will be the initial fucntion to start
        every scrapper
        """
        raise NotImplementedError

    def update_logs_in_db(self, time_taken_by_scrapper, leads_collected, id, logger):
        """Update Scrapper Logs
        """
        try:
            update_query = """
				UPDATE scraper_health
				SET leads_collected=%s, time_taken=%s
				WHERE id=%s
				"""
            values = (leads_collected, time_taken_by_scrapper, id,)
            self.db.execute(update_query, values)
            if logger:
                logger.info(
                    f"Details Inserted into DB leads_collected: {leads_collected} time_taken_by_scrapper {time_taken_by_scrapper}")

            print(f"Job Removed {self.name}")
            return (True, '')
        except Exception as e:
            return (False, e)

    def store_jobs(self, title=False, company="", city="", state="", job_url="", posted_date="", country="", description=""):
        """Store Jobs in DB
        """
        valid = get_title(title)
        self.logger.info(f"Valid: {valid} Title: {title} ")
        if valid:
            current_item = {
                "title": title,
                "city": city,
                "state": state,
                "country": country,
                "company_url": company,
                "lead_url": job_url,
                "lead_date": posted_date,
                "platform": self.name,
                "description": description

            }
            # add in lead list that will be processed in run()
            self.kafka_producer.publish_message(
                settings.kafka_topic, current_item)
            self.lead_collected += 1
            self.logger.info(f"Lead Collected: {self.lead_collected}")



# Decorator to log in progress jobs
def in_progress_jobs(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.name not in in_progress.get_jobs() and in_progress.get_job_count() <= settings.simutanious_scrappers:
            in_progress.add_job(self.name)
            self.logger.info(f"Job Added {self.name}")
            func(*args, **kwargs)
            in_progress.remove_job(self.name)
        else:
            self.logger.info(f"Job Already Running {self.name}")
    return wrapper