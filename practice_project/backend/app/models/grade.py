from typing import Optional
from datetime import date
from sqlalchemy import Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from practice_project.backend.app.database import Base


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    grade_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    student: Mapped["Student"] = relationship("Student", back_populates="grades")

    def __repr__(self):
        return f"<Grade(id={self.id}, subject='{self.subject}', score={self.score})>"