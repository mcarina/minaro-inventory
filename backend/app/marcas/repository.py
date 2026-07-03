from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.marcas.models.marca import Marca
from abc import ABC, abstractmethod

# INTERFACE REPOSITORY
class MarcaRepository(ABC):
    @abstractmethod
    async def get_by_id(self, marca_id: int) -> Marca | None: ...

    @abstractmethod
    async def create(self, marca: Marca) -> Marca: ...

    @abstractmethod
    async def list_all(self) -> list[Marca]: ...

    @abstractmethod
    async def update(self, marca: Marca) -> Marca: ...

    @abstractmethod
    async def delete(self, marca: Marca) -> None: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemyMarcaRepository(MarcaRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get marca by id
    async def get_by_id(self, marca_id: int) -> Marca | None:
        result = await self.db.execute(select(Marca).where(Marca.id == marca_id))
        return result.scalar_one_or_none()
        
    # create marca
    async def create(self, marca: Marca) -> Marca:
        self.db.add(marca)
        await self.db.commit()
        await self.db.refresh(marca)
        return marca

    # list all marcas
    async def list_all(self) -> list[Marca]:
        result = await self.db.execute(select(Marca))
        return result.scalars().all()

    # update marca
    async def update(self, marca: Marca) -> Marca:
        await self.db.commit()
        await self.db.refresh(marca)
        return marca

    # delete marca
    async def delete(self, marca: Marca) -> None:
        await self.db.delete(marca)
        await self.db.commit()
