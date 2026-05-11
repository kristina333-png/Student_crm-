from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.database import get_db
from practice_project.backend.app.schemas.group import GroupCreate, GroupUpdate, GroupResponse
from practice_project.backend.app.services import group_service

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/", response_model=list[GroupResponse])
async def get_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await group_service.list_groups(db, skip, limit, search)


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(group_id: int, db: AsyncSession = Depends(get_db)):
    return await group_service.get_group(db, group_id)


@router.post("/", response_model=GroupResponse, status_code=201)
async def create_group(group_data: GroupCreate, db: AsyncSession = Depends(get_db)):
    return await group_service.create_group(db, group_data)


@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(group_id: int, group_data: GroupUpdate, db: AsyncSession = Depends(get_db)):
    return await group_service.update_group(db, group_id, group_data)


@router.delete("/{group_id}", status_code=204)
async def delete_group(group_id: int, db: AsyncSession = Depends(get_db)):
    await group_service.delete_group(db, group_id)