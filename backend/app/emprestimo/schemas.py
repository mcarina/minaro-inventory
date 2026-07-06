from pydantic import BaseModel

class EmprestimoCreate(BaseModel):
    usuario_responsavel_id: int
    setor_id: int
    setor_id: int
    data_saida: str
    data_prevista: str
    data_devolucao: str | None
    status: str

class EmprestimoResponse(BaseModel):
    id: int
    usuario_responsavel_id: int
    setor_id: int
    setor_id: int
    data_saida: str
    data_prevista: str
    data_devolucao: str | None
    status: str

    class Config:
        from_attributes = True

class EmprestimoListResponse(BaseModel):
    emprestimos: list[EmprestimoResponse]

class EmprestimoUpdate(BaseModel):
    usuario_responsavel_id: int
    setor_id: int
    setor_id: int
    data_saida: str
    data_prevista: str
    data_devolucao: str | None
    status: str