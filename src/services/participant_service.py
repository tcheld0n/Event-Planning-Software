# services/participant_service.py
from src.services.base_service import BaseService
from src.repositories.participant_repository import ParticipantRepository
from src.repositories.event_repository import EventRepository
from src.factory.entity_factory import EntityFactory

class ParticipantService(BaseService):
    def __init__(self, participant_repository=None, event_repository=None):
        self.repo = participant_repository or ParticipantRepository()
        self.event_repo = event_repository or EventRepository()

    def create(self, event_id, name):  
        if event_id is None:
            raise ValueError("ID de evento inválido")
            
        event = self.event_repo.get_by_id(event_id)
        if not event:
            raise ValueError("Evento não encontrado")
        p = EntityFactory.create_participant(name, event_id)  
        saved = self.repo.add(p)
        return saved.to_dict()

    def update(self, participant_id, new_name):
        p = self.repo.get_by_id(participant_id)
        if not p:
            return None
        p.name = new_name
        updated = self.repo.add(p)
        return updated.to_dict()

    def delete(self, participant_id):
        p = self.repo.get_by_id(participant_id)
        if not p:
            return False
        self.repo.remove(p)
        return True

    def get_attendees(self, event_id):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            return None
        
        return [
            {
                "id": p.id,
                "display_name": f"{p.id}: {p.name}",
                "name": p.name,
                "event_id": p.event_id,
                "event_name": event.name
            }
            for p in event.participants
        ]