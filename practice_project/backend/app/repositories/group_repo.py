from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.models.group import Group
from practice_project.backend.app.models.student import Student


async def get_groups(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
) -> tuple[list[Group], int]:
    query = select(Group)

    if search:
        query = query.where(Group.name.ilike(f"%{search}%"))

    sort_column = getattr(Group, sort_by, Group.id)
    query = query.order_by(sort_column.desc() if order == "desc" else sort_column.asc())

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    groups = result.scalars().all()

    for group in groups:
        cnt = (await db.execute(select(func.count(Student.id)).where(Student.group_id == group.id))).scalar()
        group.student_count = cnt or 0

    return groups, total


async def get_group_by_id(db: AsyncSession, group_id: int) -> Group | None:
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalar_one_or_none()
    if group:
        cnt = (await db.execute(select(func.count(Student.id)).where(Student.group_id == group_id))).scalar()
        group.student_count = cnt or 0
    return group


async def get_group_by_name(db: AsyncSession, name: str) -> Group | None:
    result = await db.execute(select(Group).where(Group.name == name))
    return result.scalar_one_or_none()


async def create_group(db: AsyncSession, group_data) -> Group:
    group = Group(**group_data.model_dump())
    db.add(group)
    await db.commit()
    await db.refresh(group)
    group.student_count = 0
    return group


async def update_group(db: AsyncSession, group: Group, update_data) -> Group:
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(group, field, value)
    await db.commit()
    await db.refresh(group)
    return group


async def delete_group(db: AsyncSession, group: Group) -> None:
    await db.delete(group)
    await db.commit()