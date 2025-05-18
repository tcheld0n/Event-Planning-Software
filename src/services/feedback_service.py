# services/feedback_service.py
from src.services.base_service import BaseService
from src.repositories.feedback_repository import FeedbackRepository
from src.repositories.event_repository import EventRepository
from src.factory.entity_factory import EntityFactory

class FeedbackService(BaseService):
    def __init__(self, feedback_repository=None, event_repository=None):
        self.repo = feedback_repository or FeedbackRepository()
        self.event_repo = event_repository or EventRepository()

    def create(self, content, event_id):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            return None
        fb = EntityFactory.create_feedback(content, event_id)
        saved = self.repo.add(fb)
        return saved.to_dict()

    def update(self, feedback_id, content):
        fb = self.repo.get_by_id(feedback_id)
        if not fb:
            return None
        fb.content = content
        updated = self.repo.add(fb)
        return updated.to_dict()

    def delete(self, feedback_id):
        fb = self.repo.get_by_id(feedback_id)
        if not fb:
            return False
        self.repo.remove(fb)
        return True

    def get_feedback(self, event_id):
        event = self.event_repo.get_by_id(event_id)
        if not event:
            return None
        
        return [
            {
                "id": f.id,
                "display_name": f"Feedback {f.id}",
                "content": f.content,
                "event_id": f.event_id,
                "event_name": event.name
            }
            for f in event.feedbacks
        ]