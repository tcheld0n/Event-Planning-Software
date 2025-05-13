# models/participant.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    _name = Column("name", String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="participants")

    def __init__(self, name, event_id):
        self.name = name
        self.event_id = event_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("O nome do participante não pode ser vazio.")
        self._name = value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "event_id": self.event_id
        }
