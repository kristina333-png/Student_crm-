from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from practice_project.backend.app.schemas.group import GroupCreate, GroupUpdate
from practice_project.backend.app.repositories import group_repo


async def list_groups(db: AsyncSession, skip: int, limit: int, search: str | None):
    return await group_repo.get_groups(db, skip, limit, search)


async def get_group(db: AsyncSession, group_id: int):
    group = await group_repo.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Группа с id {group_id} не найдена")
    return group


async def create_group(db: AsyncSession, group_data: GroupCreate):
    existing = await group_repo.get_group_by_name(db, group_data.name)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Группа с таким названием уже существует")
    return await group_repo.create_group(db, group_data)


async def update_group(db: AsyncSession, group_id: int, update_data: GroupUpdate):
    group = await get_group(db, group_id)
    if update_data.name and update_data.name != group.name:
        existing = await group_repo.get_group_by_name(db, update_data.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Группа с таким названием уже существует")
    return await group_repo.update_group(db, group, update_data)


async def delete_group(db: AsyncSession, group_id: int):
    group = await get_group(db, group_id)
    return await group_repo.delete_group(db, group)