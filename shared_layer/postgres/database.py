# Postgres database connection
import psycopg2
from env import settings


class Database:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def get_connection(self):
        return psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

    def execute(self, query, params=None):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        connection.close()

    def fetch(self, query, params=None):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result