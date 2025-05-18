# repositories/speaker_repository.py
from src.database.db import SessionLocal
from src.models.speaker import Speaker
from .base_repository import BaseRepository

class SpeakerRepository(BaseRepository):
    def add(self, speaker: Speaker) -> Speaker:
        session = SessionLocal()
        try:
            session.add(speaker)
            session.commit()
            session.refresh(speaker)
            return speaker
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_id(self, speaker_id: int) -> Speaker | None:
        session = SessionLocal()
        try:
            return session.query(Speaker).filter(Speaker.id == speaker_id).first()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def list_all(self) -> list[Speaker]:
        session = SessionLocal()
        try:
            return session.query(Speaker).all()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove(self, speaker: Speaker) -> None:
        session = SessionLocal()
        try:
            session.delete(speaker)
            session.commit()
        finally:
            session.close()