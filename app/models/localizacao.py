from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Localizacao(Base):
    __tablename__ = "localizacoes"

    id:    Mapped[int] = mapped_column(primary_key=True)
    predio:  Mapped[str] = mapped_column(nullable=False)
    sala:  Mapped[str] = mapped_column(nullable=False)
    armario:  Mapped[str] = mapped_column(nullable=False)
    prateleira:  Mapped[str] = mapped_column(nullable=False)
    gaveta:  Mapped[str] = mapped_column(nullable=False)