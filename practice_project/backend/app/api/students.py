from fastapi import APIRouter, Depends, Query, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.database import get_db
from practice_project.backend.app.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentListResponse
from practice_project.backend.app.services import student_service
from practice_project.backend.app.auth import get_current_role, check_permission

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/", response_model=StudentListResponse)
async def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    group_id: int | None = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
    role: str = Depends(get_current_role),  # <-- добавили
):
    if not check_permission(role, "read"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await student_service.list_students(db, skip, limit, search, group_id, sort_by, order)


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db), role: str = Depends(get_current_role)):
    if not check_permission(role, "read"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await student_service.get_student(db, student_id)


@router.post("/", response_model=StudentResponse, status_code=201)
async def create_student(student_data: StudentCreate, db: AsyncSession = Depends(get_db), role: str = Depends(get_current_role)):
    if not check_permission(role, "create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await student_service.create_student(db, student_data)


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, student_data: StudentUpdate, db: AsyncSession = Depends(get_db), role: str = Depends(get_current_role)):
    if not check_permission(role, "update"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await student_service.update_student(db, student_id, student_data)


@router.delete("/{student_id}", status_code=204)
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db), role: str = Depends(get_current_role)):
    if not check_permission(role, "delete"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    await student_service.delete_student(db, student_id)