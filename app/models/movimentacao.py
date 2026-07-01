from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from app.core.database import Base
from datetime import datetime
from typing import Optional

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id:    Mapped[int] = mapped_column(primary_key=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(nullable=False)
    quantidade: Mapped[int] = mapped_column(nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(nullable=True)
    data: Mapped[datetime] = mapped_column(nullable=False)