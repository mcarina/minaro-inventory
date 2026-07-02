from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.core.database import Base
from datetime import datetime
from typing import Optional

class Patrimonio(Base):
    __tablename__ = "patrimonios"

    id:    Mapped[int] = mapped_column(primary_key=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), nullable=False)
    numero_patrimonio: Mapped[str] = mapped_column(nullable=False, unique=True)
    serial_number: Mapped[Optional[str]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)