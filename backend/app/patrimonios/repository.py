from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.patrimonios.models.patrimonio import Patrimonio
from abc import ABC, abstractmethod

# INTERFACE REPOSITORY
class PatrimonioRepository(ABC):
    @abstractmethod
    async def get_by_id(self, patrimonio_id: int) -> Patrimonio | None: ...

    @abstractmethod
    async def create(self, patrimonio: Patrimonio) -> Patrimonio: ...

    @abstractmethod
    async def list_all(self) -> list[Patrimonio]: ...

    @abstractmethod
    async def update(self, patrimonio: Patrimonio) -> Patrimonio: ...

    @abstractmethod
    async def delete(self, patrimonio: Patrimonio) -> None: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemyPatrimonioRepository(PatrimonioRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get patrimonio by id
    async def get_by_id(self, patrimonio_id: int) -> Patrimonio | None:
        result = await self.db.execute(select(Patrimonio).where(Patrimonio.id == patrimonio_id))
        return result.scalar_one_or_none()

    # create patrimonio
    async def create(self, patrimonio: Patrimonio) -> Patrimonio:
        self.db.add(patrimonio)
        await self.db.commit()
        await self.db.refresh(patrimonio)
        return patrimonio
        
    # list all patrimonios
    async def list_all(self) -> list[Patrimonio]:
        result = await self.db.execute(select(Patrimonio))
        return result.scalars().all()

    # update patrimonio
    async def update(self, patrimonio: Patrimonio) -> Patrimonio:
        await self.db.commit()
        await self.db.refresh(patrimonio)
        return patrimonio

    # delete patrimonio
    async def delete(self, patrimonio: Patrimonio) -> None:
        await self.db.delete(patrimonio)
        await self.db.commit()
