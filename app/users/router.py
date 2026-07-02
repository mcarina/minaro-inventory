from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.users.repository import SQLAlchemyUserRepository
from app.users.service import UserServiceImpl
from app.users.schemas import UserCreate, UserResponse, UserListResponse

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