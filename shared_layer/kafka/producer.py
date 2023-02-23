
import json
from kafka import KafkaProducer
from shared_layer.logger import logger
from env import settings


class KafkaProducerBridge():

    def __init__(self, bootstrap_servers=None, topic_name=None):
        """Creating Kafka Producer
        """
        # Setting bootstrap servers
        bootstrap_servers = bootstrap_servers if bootstrap_servers else settings.kafka_host + \
            ':' + settings.kafka_port

        # Setting Kafka Producer
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        # Setting topic name
        self.topic_name = topic_name if topic_name else settings.kafka_topic
        self.logger = logger.get_logger('kafka_bridge_logger')

    def publish_message(self, topic_name, value):
        """Publish message to kafka topic

        Args:
            topic_name (str): Topic name
            value (dict): Message to be published
        """
        try:
            self.producer.send(topic_name, value=value)
            self.producer.flush()
        except Exception as e:
            logger.error('Error while publishing message to kafka: {}'.format(e))
