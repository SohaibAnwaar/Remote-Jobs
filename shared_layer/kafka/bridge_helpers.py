from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer, KafkaProducer
import json
from env import settings


class KafkaBridge():

    def __init__(self, bootstrap_servers=["localhost:9092"]):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers)
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
        )
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def create_topics(self, topic_names: list) -> None:
        """Create topics if not exist

        Args:
            topic_names (list): List of topic names
        """

        existing_topic_list = self.consumer.topics()
        topic_list = []
        for topic in topic_names:
            if topic not in existing_topic_list:
                topic_list.append(
                    NewTopic(name=topic, num_partitions=3, replication_factor=3))

        try:
            if topic_list:
                self.admin_client.create_topics(
                    new_topics=topic_list, validate_only=False)
                
        except Exception as e:
            print(e)

    def delete_topics(self, topic_names):
        """Delete topics
        """
        try:
            self.admin_client.delete_topics(topics=topic_names)
        except Exception as e:
            print(e)

