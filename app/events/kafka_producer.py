from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

class EventProducer:

    @staticmethod
    def publish(topic: str, event: dict):

        producer.send(topic, event)

        producer.flush()