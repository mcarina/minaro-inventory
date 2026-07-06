from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.movimentacoes.models.movimentacao import Movimentacao
from abc import ABC, abstractmethod

# INTERFACE REPOSITORY
class MovimentacaoRepository(ABC):
    @abstractmethod
    async def get_by_id(self, movimentacao_id: int) -> Movimentacao | None: ...

    @abstractmethod
    async def create(self, movimentacao: Movimentacao) -> Movimentacao: ...

    @abstractmethod
    async def list_all(self) -> list[Movimentacao]: ...

    @abstractmethod
    async def update(self, movimentacao: Movimentacao) -> Movimentacao: ...

    @abstractmethod
    async def delete(self, movimentacao: Movimentacao) -> None: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemyMovimentacaoRepository(MovimentacaoRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get movimentacao by id
    async def get_by_id(self, movimentacao_id: int) -> Movimentacao | None:
        result = await self.db.execute(select(Movimentacao).where(Movimentacao.id == movimentacao_id))
        return result.scalar_one_or_none()

    # create movimentacao
    async def create(self, movimentacao: Movimentacao) -> Movimentacao:
        self.db.add(movimentacao)
        await self.db.commit()
        await self.db.refresh(movimentacao)
        return movimentacao
        
    # list all movimentacoes
    async def list_all(self) -> list[Movimentacao]:
        result = await self.db.execute(select(Movimentacao))
        return result.scalars().all()

    # update movimentacao
    async def update(self, movimentacao: Movimentacao) -> Movimentacao:
        await self.db.commit()
        await self.db.refresh(movimentacao)
        return movimentacao

    # delete movimentacao
    async def delete(self, movimentacao: Movimentacao) -> None:
        await self.db.delete(movimentacao)
        await self.db.commit()
