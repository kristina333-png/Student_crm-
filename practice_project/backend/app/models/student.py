from typing import Optional, List
from datetime import date
from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from practice_project.backend.app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    group_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("groups.id"), nullable=True)
    enrollment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    group: Mapped[Optional["Group"]] = relationship("Group", back_populates="students")
    grades: Mapped[List["Grade"]] = relationship(
        "Grade", back_populates="student", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.first_name} {self.last_name}')>"