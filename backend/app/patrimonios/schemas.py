from pydantic import BaseModel

class PatrimonioCreate(BaseModel):
    produto_id: int
    status: str
    numero_patrimonio: str
    serial_number: str | None

class PatrimonioResponse(BaseModel):
    id: int
    produto_id: int
    status: str
    numero_patrimonio: str | None
    serial_number: str | None

    class Config:
        from_attributes = True

class PatrimonioListResponse(BaseModel):
    patrimonios: list[PatrimonioResponse]

class PatrimonioUpdate(BaseModel):
    produto_id: int
    status: str
    numero_patrimonio: str | None
    serial_number: str | None