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
        print(list(self.consumer.topics()))
        topic_list = []
        for topic in topic_names:
            if topic not in existing_topic_list:
                print('Topic : {} added '.format(topic))
                topic_list.append(
                    NewTopic(name=topic, num_partitions=3, replication_factor=3))
            else:
                print('Topic : {topic} already exist ')
        try:
            if topic_list:
                self.admin_client.create_topics(
                    new_topics=topic_list, validate_only=False)
                print("Topic Created Successfully")
            else:
                print("Topic Exist")
        except Exception as e:
            print(e)

    def delete_topics(self, topic_names):
        """Delete topics
        """
        try:
            self.admin_client.delete_topics(topics=topic_names)
            print("Topic Deleted Successfully")
        except Exception as e:
            print(e)


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

    def publish_message(self, topic_name, value):
        """Publish message to kafka topic

        Args:
            topic_name (str): Topic name
            value (dict): Message to be published
        """
        try:
            print("Topics Name: ", topic_name)
            self.producer.send(topic_name, value=value)
            self.producer.flush()
            print("Message Published Successfully")
        except Exception as e:
            print(e)
