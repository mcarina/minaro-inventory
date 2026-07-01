from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Role(Base):
    __tablename__ = "roles"

    id:    Mapped[int] = mapped_column(primary_key=True)
    nome:  Mapped[str] = mapped_column(nullable=False, unique=True)