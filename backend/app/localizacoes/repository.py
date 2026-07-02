from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.localizacoes.models.localizacao import Localizacao
from abc import ABC, abstractmethod

# INTERFACE REPOSITORY
class LocalizacaoRepository(ABC):
    @abstractmethod
    async def get_by_id(self, localizacao_id: int) -> Localizacao | None: ...

    @abstractmethod
    async def create(self, localizacao: Localizacao) -> Localizacao: ...

    @abstractmethod
    async def list_all(self) -> list[Localizacao]: ...

    @abstractmethod
    async def update(self, localizacao: Localizacao) -> Localizacao: ...

    @abstractmethod
    async def delete(self, localizacao: Localizacao) -> None: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemyLocalizacaoRepository(LocalizacaoRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get localizacao by id
    async def get_by_id(self, localizacao_id: int) -> Localizacao | None:
        result = await self.db.execute(select(Localizacao).where(Localizacao.id == localizacao_id))
        return result.scalar_one_or_none()
        
    # create localizacao
    async def create(self, localizacao: Localizacao) -> Localizacao:
        self.db.add(localizacao)
        await self.db.commit()
        await self.db.refresh(localizacao)
        return localizacao

    # list all localizacoes
    async def list_all(self) -> list[Localizacao]:
        result = await self.db.execute(select(Localizacao))
        return result.scalars().all()

    # update localizacao
    async def update(self, localizacao: Localizacao) -> Localizacao:
        await self.db.commit()
        await self.db.refresh(localizacao)
        return localizacao

    # delete categoria
    async def delete(self, localizacao: Localizacao) -> None:
        await self.db.delete(localizacao)
        await self.db.commit()
