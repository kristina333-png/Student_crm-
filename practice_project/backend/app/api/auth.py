from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from practice_project.backend.app.database import get_db
from practice_project.backend.app.schemas.user import UserLogin, UserRegister, UserResponse
from practice_project.backend.app.services import auth_service
from practice_project.backend.app.auth_jwt.current_user import get_current_user
from practice_project.backend.app.models.user import User

router = APIRouter(prefix="/auth_jwt", tags=["auth_jwt"])


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await auth_service.login(db, data)


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    data: UserRegister,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Только администратор может создавать новых пользователей
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администратор может создавать пользователей"
        )
    return await auth_service.register(db, data)