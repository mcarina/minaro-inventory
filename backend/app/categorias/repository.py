from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.categorias.models.categoria import Categoria
from abc import ABC, abstractmethod

# INTERFACE REPOSITORY
class CategoriaRepository(ABC):
    @abstractmethod
    async def get_by_id(self, categoria_id: int) -> Categoria | None: ...

    @abstractmethod
    async def create(self, categoria: Categoria) -> Categoria: ...

    @abstractmethod
    async def list_all(self) -> list[Categoria]: ...

    @abstractmethod
    async def update(self, categoria: Categoria) -> Categoria: ...

    @abstractmethod
    async def delete(self, categoria: Categoria) -> None: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemyCategoriaRepository(CategoriaRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get categoria by id
    async def get_by_id(self, categoria_id: int) -> Categoria | None:
        result = await self.db.execute(select(Categoria).where(Categoria.id == categoria_id))
        return result.scalar_one_or_none()
        
    # create categoria
    async def create(self, categoria: Categoria) -> Categoria:
        self.db.add(categoria)
        await self.db.commit()
        await self.db.refresh(categoria)
        return categoria

    # list all categorias
    async def list_all(self) -> list[Categoria]:
        result = await self.db.execute(select(Categoria))
        return result.scalars().all()

    # update categoria
    async def update(self, categoria: Categoria) -> Categoria:
        await self.db.commit()
        await self.db.refresh(categoria)
        return categoria

    # delete categoria
    async def delete(self, categoria: Categoria) -> None:
        await self.db.delete(categoria)
        await self.db.commit()
