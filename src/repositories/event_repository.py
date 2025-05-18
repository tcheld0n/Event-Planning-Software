# repositories/event_repository.py
from sqlalchemy.orm import joinedload
from src.database.db import SessionLocal
from src.models.event import Event

class EventRepository:
    def __init__(self):
        self._Session = SessionLocal

    def add(self, event: Event):
        session = self._Session()
        try:
            session.add(event)
            session.commit()
            session.refresh(event)
            return event
        finally:
            session.close()

    def get_by_id(self, event_id: int) -> Event | None:
        session = self._Session()
        try:
            # Carrega o evento e suas relações de uma só vez
            return session.query(Event)\
                .options(
                    joinedload(Event.participants),
                    joinedload(Event.speakers),
                    joinedload(Event.vendors),
                    joinedload(Event.feedbacks)
                )\
                .filter(Event.id == event_id).first()
        finally:
            session.close()

    def list_all(self) -> list[Event]:
        session = self._Session()
        try:
            return session.query(Event).all()
        finally:
            session.close()

    def remove(self, event: Event):
        session = self._Session()
        try:
            session.delete(event)
            session.commit()
        finally:
            session.close()