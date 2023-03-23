# Implementation of Kafka Bridge

from env import settings
from kafka import KafkaConsumer, KafkaProducer
from json import loads
from shared_layer.postgres.database import Database
import threading
from shared_layer.logger import logger
import time


class KafkaConsumerBridge():

    def __init__(self) -> None:
        self.logger = logger.get_logger('kafka_bridge_logger')
        self.consumer = KafkaConsumer(
            settings.kafka_topic,
            bootstrap_servers=[settings.kafka_host +
                               ':' + settings.kafka_port],
            
            auto_offset_reset='earliest',
            group_id=None,
            value_deserializer=lambda x: loads(x.decode('utf-8')))
        self.logger.info('Kafka consumer initialized')

        self.db = Database()

    def kafka_to_postgres(self):
        """Storing leads from kafka to postgres
        """
        while True:
            try:
                record = self.consumer.poll(timeout_ms=1000)
                for topic_partition, messages in record.items():
                    for message in messages:
                        st_time = time.time()
                        message = message.value
                        # Check if lead already exists
                        query = 'SELECT * FROM leads WHERE lead_url = %s'
                        results = self.db.fetch(
                            query=query, params=(message['lead_url'],))
                        if results:
                            self.logger.info('Time taken: {}, status: {} '.format(
                                time.time() - st_time, 'Already exists'))
                            continue

                        query = 'INSERT INTO leads (title,  city, state, country, lead_date, lead_url, company_url, platform, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                        values = (message['title'], message['city'], message['state'], message['country'],
                                  message['lead_date'], message['lead_url'], message['company_url'], message['platform'], message['description'])
                        self.db.execute(query=query, params=values)
                        self.logger.info('Time taken: {}, status: {} '.format(
                            time.time() - st_time, 'success'))
            except Exception as e:
                self.logger.error(e)
                self.logger.error('Time taken: {}, status: {} Query executed: {} '.format(
                    time.time() - st_time, query, 'failed'))



