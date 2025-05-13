from database.db import SessionLocal
from models.feedback import Feedback
from models.event import Event
from services.base_service import BaseService

class FeedbackService(BaseService):
    def create(self, event_id, content):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            feedback = Feedback(content=content, event_id=event_id)
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            return feedback.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def update(self, feedback_id, content):
        session = SessionLocal()
        try:
            feedback = session.query(Feedback).filter(Feedback.id == feedback_id).first()
            if not feedback:
                return None
            feedback.content = content
            session.commit()
            return feedback.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self, feedback_id):
        session = SessionLocal()
        try:
            feedback = session.query(Feedback).filter(Feedback.id == feedback_id).first()
            if not feedback:
                return False
            session.delete(feedback)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
