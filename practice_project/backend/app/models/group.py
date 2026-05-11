from typing import Optional, List
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from practice_project.backend.app.database import Base


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    students: Mapped[List["Student"]] = relationship(
        "Student", back_populates="group", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"