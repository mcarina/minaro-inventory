from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.estoques.models.estoque import Estoque
from abc import ABC, abstractmethod

# INTERFACE REPOSITORY
class EstoqueRepository(ABC):
    @abstractmethod
    async def get_by_id(self, estoque_id: int) -> Estoque | None: ...

    @abstractmethod
    async def create(self, estoque: Estoque) -> Estoque: ...

    @abstractmethod
    async def list_all(self) -> list[Estoque]: ...

    @abstractmethod
    async def update(self, estoque: Estoque) -> Estoque: ...

    @abstractmethod
    async def delete(self, estoque: Estoque) -> None: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemyEstoqueRepository(EstoqueRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get estoque by id
    async def get_by_id(self, estoque_id: int) -> Estoque | None:
        result = await self.db.execute(select(Estoque).where(Estoque.id == estoque_id))
        return result.scalar_one_or_none()

    # create estoque
    async def create(self, estoque: Estoque) -> Estoque:
        self.db.add(estoque)
        await self.db.commit()
        await self.db.refresh(estoque)
        return estoque
        
    # list all estoques
    async def list_all(self) -> list[Estoque]:
        result = await self.db.execute(select(Estoque))
        return result.scalars().all()

    # update estoque
    async def update(self, estoque: Estoque) -> Estoque:
        await self.db.commit()
        await self.db.refresh(estoque)
        return estoque

    # delete estoque
    async def delete(self, estoque: Estoque) -> None:
        await self.db.delete(estoque)
        await self.db.commit()
