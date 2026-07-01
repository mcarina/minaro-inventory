from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Setor(Base):
    __tablename__ = "setores"

    id:    Mapped[int] = mapped_column(primary_key=True)
    nome:  Mapped[str] = mapped_column(nullable=False, unique=True)