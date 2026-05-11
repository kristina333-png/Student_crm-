from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.models.grade import Grade


async def get_grades(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    student_id: int | None = None,
    subject: str | None = None,
):
    query = select(Grade)
    if student_id is not None:
        query = query.where(Grade.student_id == student_id)
    if subject:
        query = query.where(Grade.subject.ilike(f"%{subject}%"))
    query = query.offset(skip).limit(limit).order_by(Grade.id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_grade_by_id(db: AsyncSession, grade_id: int):
    result = await db.execute(select(Grade).where(Grade.id == grade_id))
    return result.scalar_one_or_none()


async def create_grade(db: AsyncSession, grade_data):
    grade = Grade(**grade_data.model_dump())
    db.add(grade)
    await db.commit()
    await db.refresh(grade)
    return grade


async def update_grade(db: AsyncSession, grade: Grade, update_data):
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(grade, field, value)
    await db.commit()
    await db.refresh(grade)
    return grade


async def delete_grade(db: AsyncSession, grade: Grade):
    await db.delete(grade)
    await db.commit()
    return grade