from pydantic import BaseModel

# criando uma produto/ post
class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    categoria_id: int
    marca_id: int
    codigo_interno: str
    codigo_barras: str | None = None
    modelo: str | None = None
    localizacao_id: int
    estoque_minimo: int
    ativo: bool = True

# resposta do produto/ get
class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    categoria_id: int
    marca_id: int
    codigo_interno: str
    codigo_barras: str | None = None
    modelo: str | None = None
    localizacao_id: int
    estoque_minimo: int
    ativo: bool = True

    class Config:
        from_attributes = True

# Listagem de Produtos/ get
class ProdutoListResponse(BaseModel):
    produtos: list[ProdutoResponse]

# atualizacao do produto/ patch
class ProdutoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    categoria_id: int | None = None
    marca_id: int | None = None
    codigo_interno: str | None = None
    codigo_barras: str | None = None
    modelo: str | None = None
    localizacao_id: int | None = None
    estoque_minimo: int | None = None
    ativo: bool | None = None