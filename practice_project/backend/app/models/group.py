from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"