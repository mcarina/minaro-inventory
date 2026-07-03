from abc import ABC, abstractmethod
from app.setores.models.setor import Setor
from app.setores.repository import SetorRepository

# Service Interface
class SetorService(ABC):
    @abstractmethod
    async def create_setor(
        self, 
        nome: str,
        ) -> Setor: ...

    @abstractmethod
    async def get_by_id(self, setor_id: int) -> Setor | None: ...
    
    @abstractmethod
    async def list_setores(self) -> list[Setor]: ...

    @abstractmethod
    async def update_setor(
        self,
        setor_id: int,
        nome: str | None = None
    ) -> Setor | None: ...

    @abstractmethod
    async def delete_setor(self, setor_id: int) -> bool: ...
    
# Service Implementation
class SetorServiceImpl(SetorService):
    def __init__(self, repository: SetorRepository):
        self.repository = repository

    # create setor service
    async def create_setor(
        self, 
        nome: str,
        ) -> Setor:
        setor = Setor(
            nome=nome
        )
        return await self.repository.create(setor)

    # get setor by id service
    async def get_by_id(self, setor_id: int) -> Setor | None:
        return await self.repository.get_by_id(setor_id)

    # list all setores service
    async def list_setores(self) -> list[Setor]:
        return await self.repository.list_all()

    # update setor service
    async def update_setor(
        self,
        setor_id: int,
        nome: str | None = None
    ) -> Setor | None:
        setor = await self.repository.get_by_id(setor_id)
        if setor is None:
            return None
        if nome is not None:
            setor.nome = nome
        return await self.repository.update(setor)

    # delete setor service
    async def delete_setor(self, setor_id: int) -> bool:
        setor = await self.repository.get_by_id(setor_id)
        if setor is None:
            return False
        await self.repository.delete(setor)
        return True
