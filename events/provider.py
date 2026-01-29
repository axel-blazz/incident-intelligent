from .kafka_dispatcher import KafkaEventDispatcher
from .dispatcher import EventDispatcher

_event_dispatcher: EventDispatcher | None = None

def get_event_dispatcher() -> EventDispatcher:
    global _event_dispatcher
    if _event_dispatcher is None:
        _event_dispatcher = KafkaEventDispatcher(
            bootstrap_servers="localhost:9092",
            topic="incident.events"
        )
    return _event_dispatcher