from abc import ABC, abstractmethod
from app.patrimonios.models.patrimonio import Patrimonio
from app.patrimonios.repository import PatrimonioRepository

# Service Interface
class PatrimonioService(ABC):
    @abstractmethod
    async def create_patrimonio(
        self,
        produto_id: int,
        status: str,
        numero_patrimonio: str | None,
        serial_number: str | None,
        ) -> Patrimonio: ...

    @abstractmethod
    async def get_by_id(self, patrimonio_id: int) -> Patrimonio | None: ...
    @abstractmethod
    async def list_all(self) -> list[Patrimonio]: ...

    @abstractmethod
    async def update(
        self,
        patrimonio_id: int,
        produto_id: int | None = None,
        status: str | None = None,
        numero_patrimonio: str | None = None,
        serial_number: str | None = None,
    ) -> Patrimonio | None: ...

    @abstractmethod
    async def delete(self, patrimonio_id: int) -> bool: ...
    
# Service Implementation
class PatrimonioServiceImpl(PatrimonioService):
    def __init__(self, repository: PatrimonioRepository):
        self.repository = repository

    # create patrimonio service
    async def create_patrimonio(
        self,
        produto_id: int,
        status: str,
        numero_patrimonio: str,
        serial_number: str,
    ) -> Patrimonio:
        patrimonio = Patrimonio(
            produto_id=produto_id,
            status=status,
            numero_patrimonio=numero_patrimonio,
            serial_number=serial_number
        )
        return await self.repository.create(patrimonio)

    # get patrimonio by id service
    async def get_by_id(self, patrimonio_id: int) -> Patrimonio | None:
        return await self.repository.get_by_id(patrimonio_id)

    # list all patrimonios service
    async def list_all(self) -> list[Patrimonio]:
        return await self.repository.list_all()

    # update patrimonio service
    async def update(
        self,
        patrimonio_id: int,
        produto_id: int | None = None,
        status: str | None = None,
        numero_patrimonio: str | None = None,
        serial_number: str | None = None,
    ) -> Patrimonio | None:
        patrimonio = await self.repository.get_by_id(patrimonio_id)
        if patrimonio is None:
            return None
        if produto_id is not None:
            patrimonio.produto_id = produto_id
        if status is not None:
            patrimonio.status = status
        if numero_patrimonio is not None:
            patrimonio.numero_patrimonio = numero_patrimonio
        if serial_number is not None:
            patrimonio.serial_number = serial_number
        return await self.repository.update(patrimonio)

        
    # delete patrimonio service
    async def delete(self, patrimonio_id: int) -> bool:
        patrimonio = await self.repository.get_by_id(patrimonio_id)
        if patrimonio is None:
            return False
        await self.repository.delete(patrimonio)
        return True
