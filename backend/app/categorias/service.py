from abc import ABC, abstractmethod
from app.categorias.models.categoria import Categoria
from app.categorias.repository import CategoriaRepository

# Service Interface
class CategoriaService(ABC):
    @abstractmethod
    async def create_categoria(self, nome: str, descricao: str) -> Categoria: ...

    @abstractmethod
    async def get_by_id(self, categoria_id: int) -> Categoria | None: ...

    @abstractmethod
    async def list_categorias(self) -> list[Categoria]: ...

    @abstractmethod
    async def update_categoria(
        self,
        categoria_id: int,
        nome: str | None = None,
        descricao: str | None = None,
    ) -> Categoria | None: ...

    @abstractmethod
    async def delete_categoria(self, categoria_id: int) -> bool: ...

# Service Implementation
class CategoriaServiceImpl(CategoriaService):
    def __init__(self, repository: CategoriaRepository):
        self.repository = repository

    # create categoria service
    async def create_categoria(self, nome: str, descricao: str) -> Categoria:
        categoria = Categoria(nome=nome, descricao=descricao)
        return await self.repository.create(categoria)

    # get categoria by id service
    async def get_by_id(self, categoria_id: int) -> Categoria | None:
        return await self.repository.get_by_id(categoria_id)

    # list all categorias service
    async def list_categorias(self) -> list[Categoria]:
        return await self.repository.list_all()

    # update categoria service
    async def update_categoria(
        self,
        categoria_id: int,
        nome: str | None = None,
        descricao: str | None = None,
    ) -> Categoria | None:
        categoria = await self.repository.get_by_id(categoria_id)
        if categoria is None:
            return None

        if nome is not None:
            categoria.nome = nome
        if descricao is not None:
            categoria.descricao = descricao

        return await self.repository.update(categoria)

    # delete categoria service
    async def delete_categoria(self, categoria_id: int) -> bool:
        categoria = await self.repository.get_by_id(categoria_id)
        if categoria is None:
            return False

        await self.repository.delete(categoria)
        return True