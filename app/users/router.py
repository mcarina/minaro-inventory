from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.users.repository import SQLAlchemyUserRepository
from app.users.service import UserServiceImpl
from app.users.schemas import UserCreate, UserResponse, UserListResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserServiceImpl:
    repository = SQLAlchemyUserRepository(db)
    return UserServiceImpl(repository)

# rota post, create user
@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    data: UserCreate,
    service: UserServiceImpl = Depends(get_user_service),
):
    try:
        return await service.create_user(data.nome, data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

# rota get, get list of users
@router.get("/", response_model=UserListResponse)
async def list_users(
    service: UserServiceImpl = Depends(get_user_service),
):
    users = await service.list_users()
    return UserListResponse(users=users)

# rota get by id
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, service: UserServiceImpl = Depends(get_user_service)):
    user = await service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="usuário não encontrado")
    return user

# rota patch, update user
@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserServiceImpl = Depends(get_user_service),
):
    try:
        user = await service.update_user(
            user_id,
            nome=data.nome,
            email=data.email,
            password=data.password,
            ativo=data.ativo,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if user is None:
        raise HTTPException(status_code=404, detail="usuário não encontrado")
    return user

# rota delete, delete user
@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, service: UserServiceImpl = Depends(get_user_service)):
    success = await service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="usuário não encontrado")