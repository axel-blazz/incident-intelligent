import json
from uuid import UUID
from schemas.incidents import IncidentOut
from cache.factory import get_cache_backend
from cache.namespace_cache import NamespaceCache


TTL_SECONDS = 300

incident_cache = NamespaceCache(prefix="incident", backend=get_cache_backend())

def get_incident_from_cache(incident_id: UUID) -> IncidentOut | None:
    raw = incident_cache.get(str(incident_id))
    if raw is None:
        return None
    data = json.loads(raw)
    return IncidentOut(**data)

def set_incident_in_cache(incident: IncidentOut) -> None:
    incident_cache.set(
        key=str(incident.id),
        value=incident.model_dump_json(),
        ttl=TTL_SECONDS
    )

def delete_incident_from_cache(incident_id: UUID) -> None:
    incident_cache.delete(str(incident_id))