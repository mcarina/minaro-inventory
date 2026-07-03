from pydantic import BaseModel

# criando uma marca/ post
class MarcaCreate(BaseModel):
    nome: str

# resposta da Marca/ get
class MarcaResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

# Listagem de Marcas/ get
class MarcaListResponse(BaseModel):
    marcas: list[MarcaResponse]

# atualizacao da Marca/ patch
class MarcaUpdate(BaseModel):
    nome: str | None = None
