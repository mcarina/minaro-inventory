from pydantic import BaseModel
from datetime import datetime

class MovimentacaoCreate(BaseModel):
    produto_id: int
    user_id: int
    tipo: str
    quantidade: int
    data: datetime
    motivo: str

class MovimentacaoResponse(BaseModel):
    id: int
    produto_id: int
    user_id: int
    tipo: str
    quantidade: int
    data: datetime
    motivo: str

    class Config:
        from_attributes = True

class MovimentacaoListResponse(BaseModel):
    movimentacoes: list[MovimentacaoResponse]

class MovimentacaoUpdate(BaseModel):
    produto_id: int
    user_id: int
    tipo: str
    quantidade: int
    data: datetime
    motivo: str