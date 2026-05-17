from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from practice_project.backend.app.schemas.grade import GradeCreate, GradeUpdate
from practice_project.backend.app.repositories import grade_repo, student_repo
from practice_project.backend.app.logger import logger


async def list_grades(
    db: AsyncSession, skip: int, limit: int,
    student_id: int | None, subject: str | None,
    sort_by: str, order: str,
) -> dict:
    grades, total = await grade_repo.get_grades(db, skip, limit, student_id, subject, sort_by, order)
    return {
        "items": grades,
        "total": total,
        "page": skip // limit + 1 if limit else 1,
        "limit": limit,
        "pages": (total + limit - 1) // limit if limit else 1,
    }


async def get_grade(db: AsyncSession, grade_id: int):
    grade = await grade_repo.get_grade_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Оценка с id {grade_id} не найдена")
    return grade


async def create_grade(db: AsyncSession, grade_data: GradeCreate):
    student = await student_repo.get_student_by_id(db, grade_data.student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Студент с id {grade_data.student_id} не найден")
    grade = await grade_repo.create_grade(db, grade_data)
    logger.info(f"Создана оценка: {grade.subject} {grade.score} (id={grade.id})")
    return grade


async def update_grade(db: AsyncSession, grade_id: int, update_data: GradeUpdate):
    grade = await get_grade(db, grade_id)
    updated = await grade_repo.update_grade(db, grade, update_data)
    logger.info(f"Обновлена оценка: id={grade_id}")
    return updated


async def delete_grade(db: AsyncSession, grade_id: int) -> None:
    grade = await get_grade(db, grade_id)
    await grade_repo.delete_grade(db, grade)
    logger.info(f"Удалена оценка: id={grade_id}")