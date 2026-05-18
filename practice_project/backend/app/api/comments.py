from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.database import get_db
from practice_project.backend.app.schemas.comment import CommentCreate, CommentResponse
from practice_project.backend.app.services import comment_service
from practice_project.backend.app.auth_jwt.current_user import get_current_user
from practice_project.backend.app.auth import check_permission
from practice_project.backend.app.models.user import User

router = APIRouter(prefix="/students/{student_id}/comments", tags=["comments"])


@router.get("/", response_model=list[CommentResponse])
async def get_comments(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_permission(current_user.role, "read"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await comment_service.get_comments(db, student_id)


@router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(
    student_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_permission(current_user.role, "create"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    return await comment_service.create_comment(db, student_id, data)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    student_id: int,
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not check_permission(current_user.role, "delete"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    await comment_service.delete_comment(db, comment_id)