from pydantic import BaseModel

class EstoqueCreate(BaseModel):
    produto_id: int
    quantidade: int

class EstoqueResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int

    class Config:
        from_attributes = True

class EstoqueListResponse(BaseModel):
    estoques: list[EstoqueResponse]

# atualizacao do estoque/ patch
class EstoqueUpdate(BaseModel):
    produto_id: int
    quantidade: int