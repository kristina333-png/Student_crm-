from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    enrollment_date = Column(Date, nullable=True)

    # Связи
    group = relationship("Group", backref="students")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.first_name} {self.last_name}')>"