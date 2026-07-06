from abc import ABC, abstractmethod
from app.movimentacoes.models.movimentacao import Movimentacao
from app.movimentacoes.repository import MovimentacaoRepository
from datetime import datetime

# Service Interface
class MovimentacaoService(ABC):
    @abstractmethod
    async def create_movimentacao(
        self,
        produto_id: int,
        user_id: int,
        tipo: str,
        quantidade: int,
        data: datetime,
        motivo: str | None,
        ) -> Movimentacao: ...

    @abstractmethod
    async def get_by_id(self, movimentacao_id: int) -> Movimentacao | None: ...

    @abstractmethod
    async def list_all(self) -> list[Movimentacao]: ...

    @abstractmethod
    async def update(
        self,
        movimentacao_id: int,
        produto_id: int,
        user_id: int,
        tipo: str,
        quantidade: int,
        data: datetime,
        motivo: str | None,
    ) -> Movimentacao | None: ...

    @abstractmethod
    async def delete(self, movimentacao_id: int) -> bool: ...
    
# Service Implementation
class MovimentacaoServiceImpl(MovimentacaoService):
    def __init__(self, repository: MovimentacaoRepository):
        self.repository = repository

    # create movimentacao service
    async def create_movimentacao(
        self,
        produto_id: int,
        user_id: int,
        tipo: str,
        quantidade: int,
        data: datetime,
        motivo: str | None,
    ) -> Movimentacao:
        movimentacao = Movimentacao(
            produto_id=produto_id,
            user_id=user_id,
            tipo=tipo,
            quantidade=quantidade,
            data=data,
            motivo=motivo,
        )
        return await self.repository.create(movimentacao)

    # get movimentacao by id service
    async def get_by_id(self, movimentacao_id: int) -> Movimentacao | None:
        return await self.repository.get_by_id(movimentacao_id)

    # list all movimentacoes service
    async def list_all(self) -> list[Movimentacao]:
        return await self.repository.list_all()

    # update movimentacao service
    async def update(
        self,
        movimentacao_id: int,
        produto_id: int | None = None,
        user_id: int | None = None,
        tipo: str | None = None,
        quantidade: int | None = None,
        data: datetime | None = None,
        motivo: str | None = None,
    ) -> Movimentacao | None:
        movimentacao = await self.repository.get_by_id(movimentacao_id)
        if movimentacao is None:
            return None
        if produto_id is not None:
            movimentacao.produto_id = produto_id
        if user_id is not None:
            movimentacao.user_id = user_id
        if tipo is not None:
            movimentacao.tipo = tipo
        if quantidade is not None:
            movimentacao.quantidade = quantidade
        if data is not None:
            movimentacao.data = data
        if motivo is not None:
            movimentacao.motivo = motivo
        return await self.repository.update(movimentacao)
        
    # delete movimentacao service
    async def delete(self, movimentacao_id: int) -> bool:
        movimentacao = await self.repository.get_by_id(movimentacao_id)
        if movimentacao is None:
            return False
        await self.repository.delete(movimentacao)
        return True
