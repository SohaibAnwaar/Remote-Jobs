import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# Postgres database connection
import psycopg2, time
from env import settings
from shared_layer.logger import logger

class Database:
    def __init__(self):
        self.host = settings.database_hostname
        self.database = settings.database_name
        self.user = settings.database_username
        self.password = settings.database_password
        self.port = settings.database_port
        self.logger = logger.get_logger('db_logger')

    def get_connection(self):
        st = time.time()
        connection = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password, port=self.port)
        self.logger.info('Connection establish time {}'.format(time.time() - st))
        return connection

    def execute(self, query, params=None):
        result = None
        try:
            st_time = time.time()
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            self.logger.info('Time taken: {}, status: {} Query executed: {} '.format(time.time() - st_time, query, 'success'))
        except Exception as e:
            self.logger.error('Time taken: {}, status: {} Query executed: {} '.format(time.time() - st_time, query, 'failed'))
            self.logger.error(e)
        return result
        
    def fetch(self, query, params=None):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result