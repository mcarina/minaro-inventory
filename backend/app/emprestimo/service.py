from abc import ABC, abstractmethod
from app.emprestimo.models.emprestimo import Emprestimo
from app.emprestimo.repository import EmprestimoRepository
from datetime import datetime

# Service Interface
class EmprestimoService(ABC):
    @abstractmethod
    async def create_emprestimo(
        self,
        produto_id: int,
        usuario_responsavel_id: int,
        setor_id: int,
        data_saida: datetime,
        data_prevista: datetime,
        data_devolucao: datetime,
        status
        ) -> Emprestimo: ...

    @abstractmethod
    async def get_by_id(self, emprestimo_id: int) -> Emprestimo | None: ...
    
    @abstractmethod
    async def list_all(self) -> list[Emprestimo]: ...

    @abstractmethod
    async def update(
        self,
        patrimonio_id: int,
        usuario_responsavel_id: int | None = None,
        setor_id: int | None = None,
        data_saida: datetime | None = None,
        data_prevista: datetime | None = None,
        data_devolucao: datetime | None = None,
        status: str | None = None
    ) -> Emprestimo | None: ...

    @abstractmethod
    async def delete(self, emprestimo_id: int) -> bool: ...
    
# Service Implementation
class EmprestimoServiceImpl(EmprestimoService):
    def __init__(self, repository: EmprestimoRepository):
        self.repository = repository

    # create emprestimo service
    async def create_emprestimo(
        self,
        produto_id: int,
        usuario_responsavel_id: int,
        setor_id: int,
        data_saida: datetime,
        data_prevista: datetime,
        data_devolucao: datetime,
        status: str
    ) -> Emprestimo:
        emprestimo = Emprestimo(
            produto_id=produto_id,
            usuario_responsavel_id=usuario_responsavel_id,
            setor_id=setor_id,
            data_saida=data_saida,
            data_prevista=data_prevista,
            data_devolucao=data_devolucao,
            status=status
        )
        return await self.repository.create(emprestimo)

    # get emprestimo by id service
    async def get_by_id(self, emprestimo_id: int) -> Emprestimo | None:
        return await self.repository.get_by_id(emprestimo_id)

    # list all emprestimos service
    async def list_all(self) -> list[Emprestimo]:
        return await self.repository.list_all()

    # get emprestimo by id service
    async def get_by_id(self, emprestimo_id: int) -> Emprestimo | None:
        return await self.repository.get_by_id(emprestimo_id)

    # list all emprestimos service
    async def list_all(self) -> list[Emprestimo]:
        return await self.repository.list_all()

    # update emprestimo service
    async def update(
        self,
        emprestimo_id: int,
        produto_id: int | None = None,
        usuario_responsavel_id: int | None = None,
        setor_id: int | None = None,
        data_saida: datetime | None = None,
        data_prevista: datetime | None = None,
        data_devolucao: datetime | None = None,
        status: str | None = None
    ) -> Emprestimo | None:
        emprestimo = await self.repository.get_by_id(emprestimo_id)
        if emprestimo is None:
            return None
        if produto_id is not None:
            emprestimo.produto_id = produto_id
        if usuario_responsavel_id is not None:
            emprestimo.usuario_responsavel_id = usuario_responsavel_id
        if setor_id is not None:
            emprestimo.setor_id = setor_id
        if data_saida is not None:
            emprestimo.data_saida = data_saida
        if data_prevista is not None:
            emprestimo.data_prevista = data_prevista
        if data_devolucao is not None:
            emprestimo.data_devolucao = data_devolucao
        if status is not None:
            emprestimo.status = status
        if numero_patrimonio is not None:
            patrimonio.numero_patrimonio = numero_patrimonio
        if serial_number is not None:
            patrimonio.serial_number = serial_number
        return await self.repository.update(emprestimo)

        
    # delete patrimonio service
    async def delete(self, patrimonio_id: int) -> bool:
        patrimonio = await self.repository.get_by_id(patrimonio_id)
        if patrimonio is None:
            return False
        await self.repository.delete(patrimonio)
        return True
