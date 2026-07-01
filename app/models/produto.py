from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from app.core.database import Base
from datetime import datetime
from typing import Optional

class Produto(Base):
    __tablename__ = "produtos"

    id:    Mapped[int] = mapped_column(primary_key=True)
    nome:  Mapped[str] = mapped_column(nullable=False)
    descricao: Mapped[str] = mapped_column(nullable=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)
    marca_id: Mapped[int] = mapped_column(ForeignKey("marcas.id"), nullable=False)
    codigo_interno: Mapped[str] = mapped_column(nullable=False, unique=True)
    codigo_barras: Mapped[Optional[str]] = mapped_column(nullable=True)
    modelo: Mapped[Optional[str]] = mapped_column(nullable=True)
    localizacao_id: Mapped[int] = mapped_column(ForeignKey("localizacoes.id"), nullable=False)
    estoque_minimo: Mapped[int] = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())