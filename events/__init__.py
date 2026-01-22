from events.dispatcher import EventDispatcher
from events.kafka_dispatcher import KafkaEventDispatcher

# event_dispatcher = EventDispatcher()

event_dispatcher = KafkaEventDispatcher(
    bootstrap_servers="localhost:9092",
    topic="incident.events"
)