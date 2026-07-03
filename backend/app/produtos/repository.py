from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.produtos.models.produto import Produto
from abc import ABC, abstractmethod

# INTERFACE REPOSITORY
class ProdutoRepository(ABC):
    @abstractmethod
    async def get_by_id(self, produto_id: int) -> Produto | None: ...

    @abstractmethod
    async def create(self, produto: Produto) -> Produto: ...

    @abstractmethod
    async def list_all(self) -> list[Produto]: ...

    @abstractmethod
    async def update(self, produto: Produto) -> Produto: ...

    @abstractmethod
    async def delete(self, produto: Produto) -> None: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemyProdutoRepository(ProdutoRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get produto by id
    async def get_by_id(self, produto_id: int) -> Produto | None:
        result = await self.db.execute(select(Produto).where(Produto.id == produto_id))
        return result.scalar_one_or_none()

    # create produto
    async def create(self, produto: Produto) -> Produto:
        self.db.add(produto)
        await self.db.commit()
        await self.db.refresh(produto)
        return produto

    # list all produtos
    async def list_all(self) -> list[Produto]:
        result = await self.db.execute(select(Produto))
        return result.scalars().all()

    # update produto
    async def update(self, produto: Produto) -> Produto:
        await self.db.commit()
        await self.db.refresh(produto)
        return produto

    # delete produto
    async def delete(self, produto: Produto) -> None:
        await self.db.delete(produto)
        await self.db.commit()
