# models/event.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    _name = Column("name", String, nullable=False)
    _date = Column("date", String, nullable=False)
    _budget = Column("budget", Integer, default=0)

    # Relacionamentos com tabelas filhas
    participants = relationship("Participant", back_populates="event", cascade="all, delete-orphan")
    speakers = relationship("Speaker", back_populates="event", cascade="all, delete-orphan")
    vendors = relationship("Vendor", back_populates="event", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="event", cascade="all, delete-orphan")

    def __init__(self, name, date, budget=0):
        self.name = name
        self.date = date
        self.budget = budget

    # Propriedade para name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("O nome do evento não pode ser vazio.")
        self._name = value

    # Propriedade para date
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not value:
            raise ValueError("A data do evento não pode ser vazia.")
        self._date = value

    # Propriedade para budget
    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        if value < 0:
            raise ValueError("O orçamento não pode ser negativo!")
        self._budget = value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "budget": self.budget,
            "participants": [p.to_dict() for p in self.participants],
            "speakers": [s.to_dict() for s in self.speakers],
            "vendors": [v.to_dict() for v in self.vendors],
            "feedbacks": [f.to_dict() for f in self.feedbacks]
        }
