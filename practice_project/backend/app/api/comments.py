from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.database import get_db
from practice_project.backend.app.schemas.comment import CommentCreate, CommentResponse
from practice_project.backend.app.services import comment_service
from practice_project.backend.app.auth import get_current_role, check_permission

router = APIRouter(prefix="/students/{student_id}/comments", tags=["comments"])


@router.get("/", response_model=list[CommentResponse])
async def get_comments(student_id: int, db: AsyncSession = Depends(get_db), role: str = Depends(get_current_role)):
    if not check_permission(role, "read"):
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await comment_service.get_comments(db, student_id)


@router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(student_id: int, data: CommentCreate, db: AsyncSession = Depends(get_db), role: str = Depends(get_current_role)):
    if not check_permission(role, "create"):
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await comment_service.create_comment(db, student_id, data)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(student_id: int, comment_id: int, db: AsyncSession = Depends(get_db), role: str = Depends(get_current_role)):
    if not check_permission(role, "delete"):
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    await comment_service.delete_comment(db, comment_id)