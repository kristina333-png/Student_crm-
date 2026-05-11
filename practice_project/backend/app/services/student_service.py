from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from practice_project.backend.app.schemas.student import StudentCreate, StudentUpdate
from practice_project.backend.app.repositories import student_repo


async def list_students(db: AsyncSession, skip: int, limit: int, search: str | None, group_id: int | None):
    return await student_repo.get_students(db, skip, limit, search, group_id)


async def get_student(db: AsyncSession, student_id: int):
    student = await student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Студент с id {student_id} не найден")
    return student


async def create_student(db: AsyncSession, student_data: StudentCreate):
    existing = await student_repo.get_student_by_email(db, student_data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Студент с таким email уже существует")
    return await student_repo.create_student(db, student_data)


async def update_student(db: AsyncSession, student_id: int, update_data: StudentUpdate):
    student = await get_student(db, student_id)
    if update_data.email and update_data.email != student.email:
        existing = await student_repo.get_student_by_email(db, update_data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Студент с таким email уже существует")
    return await student_repo.update_student(db, student, update_data)


async def delete_student(db: AsyncSession, student_id: int):
    student = await get_student(db, student_id)
    return await student_repo.delete_student(db, student)