# models/speaker.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Speaker(Base):
    __tablename__ = "speakers"

    id = Column(Integer, primary_key=True, index=True)
    _name = Column("name", String, nullable=False)
    _description = Column("description", String, nullable=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="speakers")

    def __init__(self, name, description, event_id):
        self.name = name
        self.description = description
        self.event_id = event_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("O nome do palestrante não pode ser vazio.")
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value  # Pode adicionar validações se necessário

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "event_id": self.event_id
        }


3