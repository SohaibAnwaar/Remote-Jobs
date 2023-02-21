from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer, KafkaProducer
import json


class KafkaBridge():

    def __init__(self, bootstrap_servers=["localhost:9092"]):
        self.admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        self.consumer = KafkaConsumer(
            bootstrap_servers = bootstrap_servers,
            )
        self.producer = KafkaProducer(
            bootstrap_servers = bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )

    def create_topics(self, topic_names: list)-> None:
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
                topic_list.append(NewTopic(name=topic, num_partitions=3, replication_factor=3))
            else:
                print('Topic : {topic} already exist ')
        try:
            if topic_list:
                self.admin_client.create_topics(new_topics=topic_list, validate_only=False)
                print("Topic Created Successfully")
            else:
                print("Topic Exist")
        except  Exception as e:
            print(e)

    def delete_topics(self, topic_names):
        """Delete topics
        """
        try:
            self.admin_client.delete_topics(topics=topic_names)
            print("Topic Deleted Successfully")
        except  Exception as e:
            print(e)


    # def insert_into_kafka(self, topic_name, data):
    #     """Insert data into kafka
    #     """
    #     producer = KafkaProducer(bootstrap_servers=)
    #     producer.send(topic_name, json.dumps(data).encode('utf-8'))
    #     producer.flush()

    # def get_data_from_kafka(self, topic_name):
    #     """Get data from kafka
    #     """
    #     return self.consumer(topic_name)
