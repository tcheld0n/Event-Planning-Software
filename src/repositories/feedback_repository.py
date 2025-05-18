# repositories/feedback_repository.py
from src.database.db import SessionLocal
from src.models.feedback import Feedback
from .base_repository import BaseRepository

class FeedbackRepository(BaseRepository):
    def add(self, feedback: Feedback) -> Feedback:
        session = SessionLocal()
        try:
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            return feedback
        finally:
            session.close()

    def get_by_id(self, feedback_id: int) -> Feedback | None:
        session = SessionLocal()
        try:
            return session.query(Feedback).filter(Feedback.id == feedback_id).first()
        finally:
            session.close()

    def list_all(self) -> list[Feedback]:
        session = SessionLocal()
        try:
            return session.query(Feedback).all()
        finally:
            session.close()

    def remove(self, feedback: Feedback) -> None:
        session = SessionLocal()
        try:
            session.delete(feedback)
            session.commit()
        finally:
            session.close()