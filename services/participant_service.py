from database.db import SessionLocal
from models.participant import Participant
from models.event import Event
from services.base_service import BaseService

class ParticipantService(BaseService):
    def create(self, event_id, name):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            participant = Participant(name=name, event_id=event_id)
            session.add(participant)
            session.commit()
            session.refresh(participant)
            return participant.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def update(self, participant_id, new_name):
        session = SessionLocal()
        try:
            participant = session.query(Participant).filter(Participant.id == participant_id).first()
            if not participant:
                return None
            participant.name = new_name
            session.commit()
            return participant.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self, participant_id):
        session = SessionLocal()
        try:
            participant = session.query(Participant).filter(Participant.id == participant_id).first()
            if not participant:
                return False
            session.delete(participant)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # Método adicional para obter participantes de um evento:
    def get_attendees(self, event_id):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            return [participant.to_dict() for participant in event.participants]
        finally:
            session.close()
