from database.db import SessionLocal
from models.event import Event
from datetime import datetime
from services.base_service import BaseService

class EventService(BaseService):
    def create(self, name, date, budget):
        session = SessionLocal()
        try:
            event = Event(name=name, date=date, budget=budget)
            session.add(event)
            session.commit()
            session.refresh(event)
            return event.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update(self, event_id, **data):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            if "name" in data:
                event.name = data["name"]
            if "date" in data:
                event.date = datetime.strptime(data["date"], "%d-%m-%Y").date()
            if "budget" in data:
                event.budget = int(data["budget"])
            session.commit()
            return event.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, event_id):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return False
            session.delete(event)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    # Métodos adicionais que não fazem parte do contrato abstrato, mas podem ser usados normalmente:
    def list_events(self):
        session = SessionLocal()
        try:
            events = session.query(Event).all()
            return [event.to_dict() for event in events]
        finally:
            session.close()

    def update_budget(self, event_id, amount):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            event.budget += amount
            session.commit()
            return event.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_budget(self, event_id):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            return event.budget
        finally:
            session.close()

    def edit_budget(self, event_id, new_budget):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            event.budget = new_budget
            session.commit()
            return event.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
