from abc import ABC, abstractmethod
from app.marcas.models.marca import Marca
from app.marcas.repository import MarcaRepository

# Service Interface
class MarcaService(ABC):
    @abstractmethod
    async def create_marca(
        self, 
        nome: str,
        ) -> Marca: ...

    @abstractmethod
    async def get_by_id(self, marca_id: int) -> Marca | None: ...
    
    @abstractmethod
    async def list_marcas(self) -> list[Marca]: ...

    @abstractmethod
    async def update_marca(
        self,
        marca_id: int,
        nome: str | None = None
    ) -> Marca | None: ...

    @abstractmethod
    async def delete_marca(self, marca_id: int) -> bool: ...
    
# Service Implementation
class MarcaServiceImpl(MarcaService):
    def __init__(self, repository: MarcaRepository):
        self.repository = repository

    # create marca service
    async def create_marca(
        self, 
        nome: str,
        ) -> Marca:
        marca = Marca(
            nome=nome
        )
        return await self.repository.create(marca)

    # get marca by id service
    async def get_by_id(self, marca_id: int) -> Marca | None:
        return await self.repository.get_by_id(marca_id)

    # list all marcas service
    async def list_marcas(self) -> list[Marca]:
        return await self.repository.list_all()

    # update marca service
    async def update_marca(
        self,
        marca_id: int,
        nome: str | None = None
    ) -> Marca | None:
        marca = await self.repository.get_by_id(marca_id)
        if marca is None:
            return None
        if nome is not None:
            marca.nome = nome

        return await self.repository.update(marca)

    # delete marca service
    async def delete_marca(self, marca_id: int) -> bool:
        marca = await self.repository.get_by_id(marca_id)
        if marca is None:
            return False
        await self.repository.delete(marca)
        return True
