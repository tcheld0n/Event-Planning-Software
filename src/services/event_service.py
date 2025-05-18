# services/event_service.py
from src.services.base_service import BaseService
from src.repositories.event_repository import EventRepository
from src.factory.entity_factory import EntityFactory
from src.notifications.notification_manager import notification_manager # Observer

class EventService(BaseService):
    def __init__(self, event_repository=None):
        self.repo = event_repository or EventRepository() # Injeção de depedência

    def create(self, name, date, budget):
        event = EntityFactory.create_event(name, date, budget)
        saved = self.repo.add(event)
        
        notification_manager.notify("event_created", event)  # Dispara notificação de evento criado
        return saved.to_dict()

    def update(self, event_id, **data):
        event = self.repo.get_by_id(event_id)
        if not event:
            return None
        if "name" in data:
            event.name = data["name"]
        if "date" in data:
            event.date = data["date"]
        if "budget" in data:
            event.budget = int(data["budget"])
        updated = self.repo.add(event)
        return updated.to_dict()

    def delete(self, event_id):
        event = self.repo.get_by_id(event_id)
        if not event:
            return False
        self.repo.remove(event)
        return True

    def list_events(self):
        events = self.repo.list_all()
        return [
            {
                "id": event.id,
                "display_name": f"{event.id}: {event.name}",
                "name": event.name,
                "date": event.date,
                "budget": event.budget
            }
            for event in events
        ]

    def update_budget(self, event_id, amount):
        event = self.repo.get_by_id(event_id)
        if not event:
            return None
        event.budget += amount
        updated = self.repo.add(event)
        return updated.to_dict()

    def get_budget(self, event_id):
        event = self.repo.get_by_id(event_id)
        return None if not event else event.budget

    def edit_budget(self, event_id, new_budget):
        event = self.repo.get_by_id(event_id)
        if not event:
            return None
        event.budget = new_budget
        updated = self.repo.add(event)
        return updated.to_dict()
