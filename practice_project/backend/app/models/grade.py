from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    score = Column(Float, nullable=False)  # оценка от 1 до 5
    date = Column(Date, nullable=True)

    # Связь
    student = relationship("Student", back_populates="grades")

    def __repr__(self):
        return f"<Grade(id={self.id}, subject='{self.subject}', score={self.score})>"