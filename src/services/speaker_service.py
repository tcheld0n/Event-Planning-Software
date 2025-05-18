# services/speaker_service.py

from src.services.base_service import BaseService
from src.repositories.speaker_repository import SpeakerRepository
from src.repositories.event_repository import EventRepository
from src.factory.entity_factory import EntityFactory

class SpeakerService(BaseService):
    def __init__(self, speaker_repository=None, event_repository=None):
        self.repo = speaker_repository or SpeakerRepository()
        self.event_repo = event_repository or EventRepository()

    def create(self, name, description, event_id):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            return None
        s = EntityFactory.create_speaker(name, description, event_id)
        saved = self.repo.add(s)
        return saved.to_dict()

    def update(self, speaker_id, new_name=None, new_description=None):
        s = self.repo.get_by_id(speaker_id)
        if not s:
            return None
        if new_name and new_name.strip():
            s.name = new_name
        if new_description and new_description.strip():
            s.description = new_description
        updated = self.repo.add(s)
        return updated.to_dict()

    def delete(self, speaker_id):
        s = self.repo.get_by_id(speaker_id)
        if not s:
            return False
        self.repo.remove(s)
        return True

    def list_speakers(self, event_id):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            return None
        
        return [
            {
                "id": s.id,
                "display_name": f"{s.id}: {s.name}",
                "name": s.name,
                "description": s.description,
                "event_id": s.event_id,
                "event_name": event.name
            }
            for s in event.speakers
        ]
