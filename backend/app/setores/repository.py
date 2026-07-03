from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.setores.models.setor import Setor
from abc import ABC, abstractmethod

# INTERFACE REPOSITORY
class SetorRepository(ABC):
    @abstractmethod
    async def get_by_id(self, setor_id: int) -> Setor | None: ...

    @abstractmethod
    async def create(self, setor: Setor) -> Setor: ...

    @abstractmethod
    async def list_all(self) -> list[Setor]: ...

    @abstractmethod
    async def update(self, setor: Setor) -> Setor: ...

    @abstractmethod
    async def delete(self, setor: Setor) -> None: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemySetorRepository(SetorRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get setor by id
    async def get_by_id(self, setor_id: int) -> Setor | None:
        result = await self.db.execute(select(Setor).where(Setor.id == setor_id))
        return result.scalar_one_or_none()
        
    # create setor
    async def create(self, setor: Setor) -> Setor:
        self.db.add(setor)
        await self.db.commit()
        await self.db.refresh(setor)
        return setor

    # list all setores
    async def list_all(self) -> list[Setor]:
        result = await self.db.execute(select(Setor))
        return result.scalars().all()

    # update setor
    async def update(self, setor: Setor) -> Setor:
        await self.db.commit()
        await self.db.refresh(setor)
        return setor

    # delete setor
    async def delete(self, setor: Setor) -> None:
        await self.db.delete(setor)
        await self.db.commit()
