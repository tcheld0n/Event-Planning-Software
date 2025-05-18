# repositories/participant_repository.py
from src.database.db import SessionLocal
from src.models.participant import Participant
from .base_repository import BaseRepository

class ParticipantRepository(BaseRepository):
    def add(self, participant: Participant) -> Participant:
        session = SessionLocal()
        try:
            session.add(participant)
            session.commit()
            session.refresh(participant)
            return participant
        #review excepiton rollback
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_id(self, participant_id: int) -> Participant | None:
        session = SessionLocal()
        try:
            return session.query(Participant).filter(Participant.id == participant_id).first()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def list_all(self) -> list[Participant]:
        session = SessionLocal()
        try:
            return session.query(Participant).all()
        except Exception as e:
            session.rollback()
        finally:
            session.close()

    def remove(self, participant: Participant) -> None:
        session = SessionLocal()
        try:
            session.delete(participant)
            session.commit()
        except Exception as e:
            session.rollback()
        finally:
            session.close()
