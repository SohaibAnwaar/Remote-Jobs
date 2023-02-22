from abc import ABCMeta, abstractmethod
from datetime import datetime
import time

from env import settings
from shared_layer.kafka.bridge_helpers import KafkaProducerBridge
from shared_layer.postgres.database import Database

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
		self.date_time_format ="%Y-%m-%d %H:%M:%S"
		self.instance = None
		self.delay = 1380
		self.tags = []
		self.kafka_producer = KafkaProducerBridge()
		self.name = "Main"
		self.page_limit = 4
		print(f"Initilising class {self.name}")
	
	
	def __del__(self):
		"""
		"""
		pass
	
	@classmethod
	def singleton(cls, *args, **kwargs):
		if cls._INSTANCE is None:
			cls._INSTANCE = cls.create_singleton_obj(*args, **kwargs)
		else:
			print("Object is already created")
		return cls._INSTANCE

	@classmethod
	def create_singleton_obj(cls, logger=None):  # by default None
		"""Get the singleton scraper Object

		Returns:
		Kimeta : Initialize Scraper object and return object
		"""
		print(f"Initilising class ")
		return cls(logger)
		
	@abstractmethod
	def scrap(self):
		"""Every scrapper class have run class
		which will be the initial fucntion to start
		every scrapper
		"""
		raise NotImplementedError

	def debug_architecture(self, args):
		"""Debug architecture, 
		1. Resource Handling
		2. Scrappers are running properly or not
		"""
		time.sleep(5)
		scrapper_id, id = args
		print(f"Scrapper ID: {scrapper_id} and ID: {id}")
		return True

	def publish_message(self, value):
		"""
		Publish message to the queue in Kafka
		"""
		try:
			print("Publishing message to Kafka")
			self.kafka_producer.publish_message("scrapper", value)
			return (True, None)
		except Exception as e:
			return (False, e)

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
				if logger: logger.info(f"Details Inserted into DB leads_collected: {leads_collected} time_taken_by_scrapper {time_taken_by_scrapper}")
				
				return (True, '')
			except Exception as e:
				return (False, e)






