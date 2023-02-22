# Implementation of Kafka Bridge

from env import settings
from kafka import KafkaConsumer, KafkaProducer
from json import loads
from shared_layer.postgres.database import Database

class KafkaBridge():

    def __init__(self) -> None:
        self.consumer = KafkaConsumer(
            settings.kafka_topic,
            bootstrap_servers=[settings.kafka_host + ':' + settings.kafka_port],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=settings.kafka_group_id,
            value_deserializer=lambda x: loads(x.decode('utf-8')))
        
        self.db = Database(settings.database_hostname, settings.database_name, settings.database_username, settings.database_password)
    
    def Kafka_to_postgres(self):
        for message in self.consumer:
            message = message.value
            quert = 'INSERT INTO scrapper (id, name, description, price, image_url, url) VALUES (%s, %s, %s, %s, %s, %s)'

            self.db.execute('INSERT INTO scrapper (id, name, description, price, image_url, url) VALUES (%s, %s, %s, %s, %s, %s)', (message['id'], message['name'], message['description'], message['price'], message['image_url'], message['url']))

            print('{} added'.format(message))
            return message
        

    