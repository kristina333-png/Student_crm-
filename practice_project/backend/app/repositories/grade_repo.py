from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.models.grade import Grade


async def get_grades(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    student_id: int | None = None,
    subject: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
) -> tuple[list[Grade], int]:
    query = select(Grade)

    if student_id is not None:
        query = query.where(Grade.student_id == student_id)
    if subject:
        query = query.where(Grade.subject.ilike(f"%{subject}%"))

    sort_column = getattr(Grade, sort_by, Grade.id)
    query = query.order_by(sort_column.desc() if order == "desc" else sort_column.asc())

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all(), total


async def get_grade_by_id(db: AsyncSession, grade_id: int) -> Grade | None:
    result = await db.execute(select(Grade).where(Grade.id == grade_id))
    return result.scalar_one_or_none()


async def create_grade(db: AsyncSession, grade_data) -> Grade:
    grade = Grade(**grade_data.model_dump())
    db.add(grade)
    await db.commit()
    await db.refresh(grade)
    return grade


async def update_grade(db: AsyncSession, grade: Grade, update_data) -> Grade:
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(grade, field, value)
    await db.commit()
    await db.refresh(grade)
    return grade


async def delete_grade(db: AsyncSession, grade: Grade) -> None:
    await db.delete(grade)
    await db.commit()