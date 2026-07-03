from pydantic import BaseModel

# criando uma setor/ post
class SetorCreate(BaseModel):
    nome: str

# resposta do Setor/ get
class SetorResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

# Listagem de Setores/ get
class SetorListResponse(BaseModel):
    setores: list[SetorResponse]

# atualizacao do Setor/ patch
class SetorUpdate(BaseModel):
    nome: str | None = None
