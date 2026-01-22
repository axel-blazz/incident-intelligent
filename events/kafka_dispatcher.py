import json
from confluent_kafka import Producer
from events.base import BaseEvent
from loguru import logger

class KafkaEventDispatcher:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})
        self.topic = topic
    
    def emit(self, event: BaseEvent) -> None:
        payload = event.model_dump_json()

        self.producer.produce(
            topic=self.topic,
            key=str(event.event_id).encode('utf-8'),
            value=payload.encode('utf-8'),
        )

        self.producer.poll(0) # Trigger delivery report callbacks
        logger.info(f"Emitting event to Kafka | {event.event_type} | ID: {event.event_id} | payload: {payload}")