from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.models.group import Group
from practice_project.backend.app.models.student import Student


async def get_groups(db: AsyncSession, skip: int = 0, limit: int = 100, search: str | None = None):
    query = select(Group)
    if search:
        query = query.where(Group.name.ilike(f"%{search}%"))
    query = query.offset(skip).limit(limit).order_by(Group.id)
    result = await db.execute(query)
    groups = result.scalars().all()

    for group in groups:
        count_result = await db.execute(
            select(func.count(Student.id)).where(Student.group_id == group.id)
        )
        group.student_count = count_result.scalar() or 0

    return groups


async def get_group_by_id(db: AsyncSession, group_id: int):
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalar_one_or_none()
    if group:
        count_result = await db.execute(
            select(func.count(Student.id)).where(Student.group_id == group_id)
        )
        group.student_count = count_result.scalar() or 0
    return group


async def get_group_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(Group).where(Group.name == name))
    return result.scalar_one_or_none()


async def create_group(db: AsyncSession, group_data):
    group = Group(**group_data.model_dump())
    db.add(group)
    await db.commit()
    await db.refresh(group)
    group.student_count = 0
    return group


async def update_group(db: AsyncSession, group: Group, update_data):
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(group, field, value)
    await db.commit()
    await db.refresh(group)
    return group


async def delete_group(db: AsyncSession, group: Group):
    await db.delete(group)
    await db.commit()
    return group