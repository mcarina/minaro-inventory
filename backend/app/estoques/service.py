from abc import ABC, abstractmethod
from app.estoques.models.estoque import Estoque
from app.estoques.repository import EstoqueRepository

# Service Interface
class EstoqueService(ABC):
    @abstractmethod
    async def create_estoque(
        self,
        produto_id: int,
        quantidade: int
        ) -> Estoque: ...

    @abstractmethod
    async def get_by_id(self, estoque_id: int) -> Estoque | None: ...

    @abstractmethod
    async def list_all(self) -> list[Estoque]: ...

    @abstractmethod
    async def update(
        self,
        estoque_id: int,
        produto_id: int | None = None,
        quantidade: int | None = None
    ) -> Estoque | None: ...

    @abstractmethod
    async def delete(self, estoque_id: int) -> bool: ...
    
# Service Implementation
class EstoqueServiceImpl(EstoqueService):
    def __init__(self, repository: EstoqueRepository):
        self.repository = repository

    # create estoque service
    async def create_estoque(
        self,
        produto_id: int,
        quantidade: int
    ) -> Estoque:
        estoque = Estoque(
            produto_id=produto_id,
            quantidade=quantidade
        )
        return await self.repository.create(estoque)

    # get estoque by id service
    async def get_by_id(self, estoque_id: int) -> Estoque | None:
        return await self.repository.get_by_id(estoque_id)

    # list all estoques service
    async def list_all(self) -> list[Estoque]:
        return await self.repository.list_all()

    # update estoque service
    async def update(
        self,
        estoque_id: int,
        produto_id: int | None = None,
        quantidade: int | None = None
    ) -> Estoque | None:
        estoque = await self.repository.get_by_id(estoque_id)
        if estoque is None:
            return None
        if produto_id is not None:
            estoque.produto_id = produto_id
        if quantidade is not None:
            estoque.quantidade = quantidade
        return await self.repository.update(estoque)
        
    # delete estoque service
    async def delete(self, estoque_id: int) -> bool:
        estoque = await self.repository.get_by_id(estoque_id)
        if estoque is None:
            return False
        await self.repository.delete(estoque)
        return True
