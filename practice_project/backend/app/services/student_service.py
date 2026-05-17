from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from practice_project.backend.app.schemas.student import StudentCreate, StudentUpdate
from practice_project.backend.app.repositories import student_repo
from practice_project.backend.app.logger import logger


async def list_students(
    db: AsyncSession, skip: int, limit: int, search: str | None,
    group_id: int | None, sort_by: str, order: str,
) -> dict:
    students, total = await student_repo.get_students(db, skip, limit, search, group_id, sort_by, order)
    return {
        "items": students,
        "total": total,
        "page": skip // limit + 1 if limit else 1,
        "limit": limit,
        "pages": (total + limit - 1) // limit if limit else 1,
    }


async def get_student(db: AsyncSession, student_id: int):
    student = await student_repo.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Студент с id {student_id} не найден")
    return student


async def create_student(db: AsyncSession, student_data: StudentCreate):
    existing = await student_repo.get_student_by_email(db, student_data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Студент с таким email уже существует")
    student = await student_repo.create_student(db, student_data)
    logger.info(f"Создан студент: {student.first_name} {student.last_name} (id={student.id})")
    return student


async def update_student(db: AsyncSession, student_id: int, update_data: StudentUpdate):
    student = await get_student(db, student_id)
    if update_data.email and update_data.email != student.email:
        existing = await student_repo.get_student_by_email(db, update_data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Студент с таким email уже существует")
    updated = await student_repo.update_student(db, student, update_data)
    logger.info(f"Обновлён студент: id={student_id}")
    return updated


async def delete_student(db: AsyncSession, student_id: int) -> None:
    student = await get_student(db, student_id)
    await student_repo.delete_student(db, student)
    logger.info(f"Удалён студент: id={student_id}")