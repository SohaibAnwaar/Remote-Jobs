from abc import ABCMeta, abstractmethod
from datetime import datetime
import time


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
		
		self.instance = None
		# Start after 23 hours
		self.start_after = 1380
		self.tags = []
		self.db_obj = None
		self.name = "Main"
	
	def get_db_object(self, name):
		if self.db_obj: return self.db_obj
		else: return Databases("Scrapper Main Class")


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
	def run(self):
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
		query = """delete from scrappers_health where WHERE scrapper_id=%s and id=%s"""
		self.db_obj = self.get_db_object("Main Scrapper")
		db_obj = Databases("Updating logs class Scrapper")
		db_obj.run_insert_query(query, (scrapper_id,id,))
	

	def update_logs_in_db(self, time_taken_by_scrapper, leads_collected, scrapper_id, id, logger):
		"""Update Scrapper Logs
		"""
		try:
			update_query = """
			UPDATE scrappers_health
			SET leads_collected=%s, time_taken=%s, job_ended_at=%s
			WHERE scrapper_id=%s and id=%s
			"""
			date =  datetime.now().strftime(date_time_format)
			values = (leads_collected, time_taken_by_scrapper, date,scrapper_id,id,)
			self.db_obj = self.get_db_object(f"Main Scrapper closing Scrapper {scrapper_id}")
			self.db_obj.run_insert_query(update_query, values)
			if logger: logger.info(f"Details Inserted into DB leads_collected: {leads_collected} time_taken_by_scrapper {time_taken_by_scrapper}")
			
			return (True, '')
		except Exception as e:
			return (False, e)




