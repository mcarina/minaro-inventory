from abc import ABC, abstractmethod
from app.localizacoes.models.localizacao import Localizacao
from app.localizacoes.repository import LocalizacaoRepository

# Service Interface
class LocalizacaoService(ABC):
    @abstractmethod
    async def create_localizacao(
        self, 
        predio: str, 
        sala: str,
        armario: str,
        prateleira: str,
        gaveta: str
        ) -> Localizacao: ...

    @abstractmethod
    async def get_by_id(self, localizacao_id: int) -> Localizacao | None: ...
    
    @abstractmethod
    async def list_localizacoes(self) -> list[Localizacao]: ...

    @abstractmethod
    async def update_localizacao(
        self,
        localizacao_id: int,
        predio: str | None = None,
        sala: str | None = None,
        armario: str | None = None,
        prateleira: str | None = None,
        gaveta: str | None = None
    ) -> Localizacao | None: ...

    @abstractmethod
    async def delete_localizacao(self, localizacao_id: int) -> bool: ...

# Service Implementation
class LocalizacaoServiceImpl(LocalizacaoService):
    def __init__(self, repository: LocalizacaoRepository):
        self.repository = repository

    # create localizacao service
    async def create_localizacao(
        self, 
        predio: str, 
        sala: str, 
        armario: str, 
        prateleira: str, 
        gaveta: str
        ) -> Localizacao:
        localizacao = Localizacao(
            predio=predio,
            sala=sala,
            armario=armario,
            prateleira=prateleira,
            gaveta=gaveta
        )
        return await self.repository.create(localizacao)

    # get localizacao by id service
    async def get_by_id(self, localizacao_id: int) -> Localizacao | None:
        return await self.repository.get_by_id(localizacao_id)

    # list all localizacoes service
    async def list_localizacoes(self) -> list[Localizacao]:
        return await self.repository.list_all()

    # update localizacao service
    async def update_localizacao(
        self,
        localizacao_id: int,
        predio: str | None = None,
        sala: str | None = None,
        armario: str | None = None,
        prateleira: str | None = None,
        gaveta: str | None = None
    ) -> Localizacao | None:
        localizacao = await self.repository.get_by_id(localizacao_id)
        if localizacao is None:
            return None

        if predio is not None:
            localizacao.predio = predio
        if sala is not None:
            localizacao.sala = sala
        if armario is not None:
            localizacao.armario = armario
        if prateleira is not None:
            localizacao.prateleira = prateleira
        if gaveta is not None:
            localizacao.gaveta = gaveta

        return await self.repository.update(localizacao)

    # delete localizacao service
    async def delete_localizacao(self, localizacao_id: int) -> bool:
        localizacao = await self.repository.get_by_id(localizacao_id)
        if localizacao is None:
            return False
        await self.repository.delete(localizacao)
        return True
