from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.emprestimo.models.emprestimo import Emprestimo
from abc import ABC, abstractmethod

# INTERFACE REPOSITORY
class EmprestimoRepository(ABC):
    @abstractmethod
    async def get_by_id(self, emprestimo_id: int) -> Emprestimo | None: ...

    @abstractmethod
    async def create(self, emprestimo: Emprestimo) -> Emprestimo: ...

    @abstractmethod
    async def list_all(self) -> list[Emprestimo]: ...

    @abstractmethod
    async def update(self, emprestimo: Emprestimo) -> Emprestimo: ...

    @abstractmethod
    async def delete(self, emprestimo: Emprestimo) -> None: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemyEmprestimoRepository(EmprestimoRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get emprestimo by id
    async def get_by_id(self, emprestimo_id: int) -> Emprestimo | None:
        result = await self.db.execute(select(Emprestimo).where(Emprestimo.id == emprestimo_id))
        return result.scalar_one_or_none()

    # create emprestimo
    async def create(self, emprestimo: Emprestimo) -> Emprestimo:
        self.db.add(emprestimo)
        await self.db.commit()
        await self.db.refresh(emprestimo)
        return emprestimo
        
    # list all emprestimos
    async def list_all(self) -> list[Emprestimo]:
        result = await self.db.execute(select(Emprestimo))
        return result.scalars().all()

    # update emprestimo
    async def update(self, emprestimo: Emprestimo) -> Emprestimo:
        await self.db.commit()
        await self.db.refresh(emprestimo)
        return emprestimo

    # delete emprestimo
    async def delete(self, emprestimo: Emprestimo) -> None:
        await self.db.delete(emprestimo)
        await self.db.commit()
