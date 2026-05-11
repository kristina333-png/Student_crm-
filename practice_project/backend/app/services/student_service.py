from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.student import StudentCreate, StudentUpdate
from app.repositories import student_repo


def list_students(db: Session, skip: int, limit: int, search: str | None, group_id: int | None):
    return student_repo.get_students(db, skip, limit, search, group_id)


def get_student(db: Session, student_id: int):
    student = student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Студент с id {student_id} не найден",
        )
    return student


def create_student(db: Session, student_data: StudentCreate):
    existing = student_repo.get_student_by_email(db, student_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Студент с таким email уже существует",
        )
    return student_repo.create_student(db, student_data)


def update_student(db: Session, student_id: int, update_data: StudentUpdate):
    student = get_student(db, student_id)
    if update_data.email and update_data.email != student.email:
        existing = student_repo.get_student_by_email(db, update_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Студент с таким email уже существует",
            )
    return student_repo.update_student(db, student, update_data)


def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)
    return student_repo.delete_student(db, student)