from src.models.event import Event
from src.models.participant import Participant
from src.models.feedback import Feedback
from src.models.speaker import Speaker
from src.models.vendor import Vendor

class EntityFactory():
    
    @staticmethod
    def create_event(name, date, budget):
        return Event(name=name, date=date, budget=budget)
    
    @staticmethod
    def create_participant(name, event_id):
        return Participant(name=name, event_id=event_id)
    
    @staticmethod
    def create_feedback(content, event_id):
        return Feedback(content=content, event_id=event_id)
    
    @staticmethod
    def create_speaker(name, description, event_id):
        return Speaker(name=name, description=description, event_id=event_id)
    
    @staticmethod
    def create_vendor(name, services, event_id):
        return Vendor(name=name, services=services, event_id=event_id)