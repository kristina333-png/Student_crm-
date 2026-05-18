from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.database import get_db
from practice_project.backend.app.schemas.grade import GradeCreate, GradeUpdate, GradeResponse, GradeListResponse
from practice_project.backend.app.services import grade_service
from practice_project.backend.app.auth_jwt.current_user import get_current_user
from practice_project.backend.app.auth import check_permission
from practice_project.backend.app.models.user import User

router = APIRouter(prefix="/grades", tags=["grades"])


@router.get("/", response_model=GradeListResponse)
async def get_grades(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    student_id: int | None = Query(None),
    subject: str | None = Query(None),
    sort_by: str = Query("id"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_permission(current_user.role, "read"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await grade_service.list_grades(db, skip, limit, student_id, subject, sort_by, order)


@router.get("/{grade_id}", response_model=GradeResponse)
async def get_grade(
    grade_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_permission(current_user.role, "read"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await grade_service.get_grade(db, grade_id)


@router.post("/", response_model=GradeResponse, status_code=201)
async def create_grade(
    grade_data: GradeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_permission(current_user.role, "create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await grade_service.create_grade(db, grade_data)


@router.put("/{grade_id}", response_model=GradeResponse)
async def update_grade(
    grade_id: int,
    grade_data: GradeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_permission(current_user.role, "update"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await grade_service.update_grade(db, grade_id, grade_data)


@router.delete("/{grade_id}", status_code=204)
async def delete_grade(
    grade_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_permission(current_user.role, "delete"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    await grade_service.delete_grade(db, grade_id)