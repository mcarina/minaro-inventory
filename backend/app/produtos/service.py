from abc import ABC, abstractmethod
from app.produtos.models.produto import Produto
from app.produtos.repository import ProdutoRepository

# Service Interface
class ProdutoService(ABC):
    @abstractmethod
    async def create_produto(
        self, 
        nome: str,
        descricao: str,
        categoria_id: int,
        marca_id: int,
        codigo_interno: str,
        localizacao_id: int,
        estoque_minimo: int,
        codigo_barras: str | None = None,
        modelo: str | None = None,
        ativo: bool = True
        ) -> Produto: ...

    @abstractmethod
    async def get_by_id(self, produto_id: int) -> Produto | None: ...

    @abstractmethod
    async def list_produtos(self) -> list[Produto]: ...

    @abstractmethod
    async def update_produto(
        self,
        produto_id: int,
        nome: str,
        descricao: str,
        categoria_id: int,
        marca_id: int,
        codigo_interno: str,
        localizacao_id: int,
        estoque_minimo: int,
        codigo_barras: str | None = None,
        modelo: str | None = None,
        ativo: bool = True
    ) -> Produto | None: ...

    @abstractmethod
    async def delete_produto(self, produto_id: int) -> bool: ...
    
# Service Implementation
class ProdutoServiceImpl(ProdutoService):
    def __init__(self, repository: ProdutoRepository):
        self.repository = repository

    # create produto service
    async def create_produto(
        self, 
        nome: str,
        descricao: str,
        categoria_id: int,
        marca_id: int,
        codigo_interno: str,
        localizacao_id: int,
        estoque_minimo: int,
        codigo_barras: str | None = None,
        modelo: str | None = None,
        ativo: bool = True
    ) -> Produto:
        produto = Produto(
            nome=nome,
            descricao=descricao,
            categoria_id=categoria_id,
            marca_id=marca_id,
            codigo_interno=codigo_interno,
            codigo_barras=codigo_barras,
            modelo=modelo,
            localizacao_id=localizacao_id,
            estoque_minimo=estoque_minimo,
            ativo=ativo
        )
        return await self.repository.create(produto)

    # get produto by id service
    async def get_by_id(self, produto_id: int) -> Produto | None:
        return await self.repository.get_by_id(produto_id)

    # list all produtos service
    async def list_produtos(self) -> list[Produto]:
        return await self.repository.list_all()

    # update produto service
    async def update_produto(
        self,
        produto_id: int,
        nome: str | None = None,
        descricao: str | None = None,
        categoria_id: int | None = None,
        marca_id: int | None = None,
        codigo_interno: str | None = None,
        codigo_barras: str | None = None,
        modelo: str | None = None,
        localizacao_id: int | None = None,
        estoque_minimo: int | None = None,
        ativo: bool | None = None
    ) -> Produto | None:
        produto = await self.repository.get_by_id(produto_id)
        if produto is None:
            return None
        if nome is not None:
            produto.nome = nome
        if descricao is not None:
            produto.descricao = descricao
        if categoria_id is not None:
            produto.categoria_id = categoria_id
        if marca_id is not None:
            produto.marca_id = marca_id
        if codigo_interno is not None:
            produto.codigo_interno = codigo_interno
        if codigo_barras is not None:
            produto.codigo_barras = codigo_barras
        if modelo is not None:
            produto.modelo = modelo
        if localizacao_id is not None:
            produto.localizacao_id = localizacao_id
        if estoque_minimo is not None:
            produto.estoque_minimo = estoque_minimo
        if ativo is not None:
            produto.ativo = ativo
        return await self.repository.update(produto)

    # delete produto service
    async def delete_produto(self, produto_id: int) -> bool:
        produto = await self.repository.get_by_id(produto_id)
        if produto is None:
            return False
        await self.repository.delete(produto)
        return True
