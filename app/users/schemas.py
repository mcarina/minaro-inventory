from pydantic import BaseModel, EmailStr

# criando um usuario/ post
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str

# resposta do usuario/ get
class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    ativo: bool

    class Config:
        from_attributes = True

# Listagem de usuarios/ get
class UserListResponse(BaseModel):
    users: list[UserResponse]