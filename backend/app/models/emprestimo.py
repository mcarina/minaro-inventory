from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.core.database import Base
from datetime import datetime
from typing import Optional

class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id:    Mapped[int] = mapped_column(primary_key=True)
    patrimonio_id: Mapped[int] = mapped_column(ForeignKey("patrimonios.id"), nullable=False)
    usuario_responsavel_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    setor_id: Mapped[int] = mapped_column(ForeignKey("setores.id"), nullable=False)
    data_saida: Mapped[datetime] = mapped_column(nullable=False)
    data_prevista: Mapped[datetime] = mapped_column(nullable=False)
    data_devolucao: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)