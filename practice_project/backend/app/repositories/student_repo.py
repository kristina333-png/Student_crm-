from sqlalchemy.orm import Session
from practice_project.backend.app.models.student import Student


def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    group_id: int | None = None,
):
    query = db.query(Student)
    if search:
        query = query.filter(
            Student.first_name.ilike(f"%{search}%")
            | Student.last_name.ilike(f"%{search}%")
            | Student.email.ilike(f"%{search}%")
        )
    if group_id is not None:
        query = query.filter(Student.group_id == group_id)
    return query.offset(skip).limit(limit).all()


def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()


def create_student(db: Session, student_data):
    student = Student(**student_data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student: Student, update_data):
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: Student):
    db.delete(student)
    db.commit()
    return student