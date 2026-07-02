from pydantic import BaseModel

# criando uma categoria/ post
class CategoriaCreate(BaseModel):
    nome: str
    descricao: str

# resposta da categoria/ get
class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: str

    class Config:
        from_attributes = True

# Listagem de categorias/ get
class CategoriaListResponse(BaseModel):
    categorias: list[CategoriaResponse]

# atualizacao da categoria/ patch
class CategoriaUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
