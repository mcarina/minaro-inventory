from pydantic import BaseModel
from datetime import datetime

class EmprestimoCreate(BaseModel):
    patrimonio_id: int
    usuario_responsavel_id: int
    setor_id: int
    data_saida: datetime
    data_prevista: datetime
    data_devolucao: datetime
    status: str

class EmprestimoResponse(BaseModel):
    id: int
    patrimonio_id: int
    usuario_responsavel_id: int
    setor_id: int
    data_saida: datetime
    data_prevista: datetime
    data_devolucao: datetime
    status: str

    class Config:
        from_attributes = True

class EmprestimoListResponse(BaseModel):
    emprestimos: list[EmprestimoResponse]

class EmprestimoUpdate(BaseModel):
    patrimonio_id: int
    usuario_responsavel_id: int
    setor_id: int
    data_saida: datetime
    data_prevista: datetime
    data_devolucao: datetime
    status: str