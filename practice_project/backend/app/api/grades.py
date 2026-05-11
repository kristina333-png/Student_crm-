from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.database import get_db
from practice_project.backend.app.schemas.grade import GradeCreate, GradeUpdate, GradeResponse
from practice_project.backend.app.services import grade_service

router = APIRouter(prefix="/grades", tags=["grades"])


@router.get("/", response_model=list[GradeResponse])
async def get_grades(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    student_id: int | None = Query(None),
    subject: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await grade_service.list_grades(db, skip, limit, student_id, subject)


@router.get("/{grade_id}", response_model=GradeResponse)
async def get_grade(grade_id: int, db: AsyncSession = Depends(get_db)):
    return await grade_service.get_grade(db, grade_id)


@router.post("/", response_model=GradeResponse, status_code=201)
async def create_grade(grade_data: GradeCreate, db: AsyncSession = Depends(get_db)):
    return await grade_service.create_grade(db, grade_data)


@router.put("/{grade_id}", response_model=GradeResponse)
async def update_grade(grade_id: int, grade_data: GradeUpdate, db: AsyncSession = Depends(get_db)):
    return await grade_service.update_grade(db, grade_id, grade_data)


@router.delete("/{grade_id}", status_code=204)
async def delete_grade(grade_id: int, db: AsyncSession = Depends(get_db)):
    await grade_service.delete_grade(db, grade_id)