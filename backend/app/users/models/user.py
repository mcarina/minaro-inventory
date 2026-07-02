from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id:    Mapped[int] = mapped_column(primary_key=True)
    nome:  Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())