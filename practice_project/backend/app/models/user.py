from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from practice_project.backend.app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="guest")
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)