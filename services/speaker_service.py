from database.db import SessionLocal
from models.speaker import Speaker
from models.event import Event
from services.base_service import BaseService

class SpeakerService(BaseService):
    def create(self, event_id, name, description):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            speaker = Speaker(name=name, description=description, event_id=event_id)
            session.add(speaker)
            session.commit()
            session.refresh(speaker)
            return speaker.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def update(self, speaker_id, new_name=None, new_description=None):
        session = SessionLocal()
        try:
            speaker = session.query(Speaker).filter(Speaker.id == speaker_id).first()
            if not speaker:
                return None
            if new_name and new_name.strip():
                speaker.name = new_name
            if new_description and new_description.strip():
                speaker.description = new_description
            session.commit()
            return speaker.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self, speaker_id):
        session = SessionLocal()
        try:
            speaker = session.query(Speaker).filter(Speaker.id == speaker_id).first()
            if not speaker:
                return False
            session.delete(speaker)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    # Método adicional para listar speakers de um evento:
    def list_speakers(self, event_id):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            return [speaker.to_dict() for speaker in event.speakers]
        finally:
            session.close()
