from pydantic import BaseModel


class RoleCreate(BaseModel):
    nome: str


class RoleResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    roles: list[RoleResponse]


class RoleUpdate(BaseModel):
    nome: str | None = None
