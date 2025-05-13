# models/feedback.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    _content = Column("content", String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="feedbacks")

    def __init__(self, content, event_id):
        self.content = content
        self.event_id = event_id

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not value:
            raise ValueError("O conteúdo do feedback não pode ser vazio.")
        self._content = value

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "event_id": self.event_id
        }
