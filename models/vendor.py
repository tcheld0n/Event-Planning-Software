# models/vendor.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    _name = Column("name", String, nullable=False)
    _services = Column("services", String, nullable=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="vendors")

    def __init__(self, name, services, event_id):
        self.name = name
        self.services = services
        self.event_id = event_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("O nome do fornecedor não pode ser vazio.")
        self._name = value

    @property
    def services(self):
        return self._services

    @services.setter
    def services(self, value):
        self._services = value  # Você pode adicionar validações se necessário

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "services": self.services,
            "event_id": self.event_id
        }
