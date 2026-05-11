from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from practice_project.backend.app.schemas.grade import GradeCreate, GradeUpdate
from practice_project.backend.app.repositories import grade_repo, student_repo


async def list_grades(db: AsyncSession, skip: int, limit: int, student_id: int | None, subject: str | None):
    return await grade_repo.get_grades(db, skip, limit, student_id, subject)


async def get_grade(db: AsyncSession, grade_id: int):
    grade = await grade_repo.get_grade_by_id(db, grade_id)
    if not grade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Оценка с id {grade_id} не найдена")
    return grade


async def create_grade(db: AsyncSession, grade_data: GradeCreate):
    student = await student_repo.get_student_by_id(db, grade_data.student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Студент с id {grade_data.student_id} не найден")
    return await grade_repo.create_grade(db, grade_data)


async def update_grade(db: AsyncSession, grade_id: int, update_data: GradeUpdate):
    grade = await get_grade(db, grade_id)
    return await grade_repo.update_grade(db, grade, update_data)


async def delete_grade(db: AsyncSession, grade_id: int):
    grade = await get_grade(db, grade_id)
    return await grade_repo.delete_grade(db, grade)