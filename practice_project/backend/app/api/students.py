from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.database import get_db
from practice_project.backend.app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from practice_project.backend.app.services import student_service

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/", response_model=list[StudentResponse])
async def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str | None = Query(None),
    group_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await student_service.list_students(db, skip, limit, search, group_id)


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    return await student_service.get_student(db, student_id)


@router.post("/", response_model=StudentResponse, status_code=201)
async def create_student(student_data: StudentCreate, db: AsyncSession = Depends(get_db)):
    return await student_service.create_student(db, student_data)


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, student_data: StudentUpdate, db: AsyncSession = Depends(get_db)):
    return await student_service.update_student(db, student_id, student_data)


@router.delete("/{student_id}", status_code=204)
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    await student_service.delete_student(db, student_id)