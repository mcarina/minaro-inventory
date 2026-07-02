from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.users.repository import SQLAlchemyUserRepository
from app.users.service import UserServiceImpl
from app.users.schemas import UserCreate, UserResponse, UserListResponse, UserUpdate
from app.roles.repository import SQLAlchemyRoleRepository
from app.roles.schemas import RoleListResponse
from app.users.user_role_repository import SQLAlchemyUserRoleRepository
from app.users.user_role_service import (
    UserRoleServiceImpl,
    UserNotFoundError,
    RoleNotFoundError,
    RoleAlreadyAssignedError,
    RoleNotAssignedError,
)
from app.auth.dependencies import get_current_user
from app.users.models.user import User

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
    current_user: User = Depends(get_current_user),
):
    users = await service.list_users()
    return UserListResponse(users=users)

# rota get by id
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, 
    service: UserServiceImpl = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
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
    current_user: User = Depends(get_current_user),
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
async def delete_user(user_id: int, 
    service: UserServiceImpl = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    success = await service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="usuário não encontrado")

# 
def get_user_role_service(db: AsyncSession = Depends(get_db)) -> UserRoleServiceImpl:
    user_repository = SQLAlchemyUserRepository(db)
    role_repository = SQLAlchemyRoleRepository(db)
    user_role_repository = SQLAlchemyUserRoleRepository(db)
    return UserRoleServiceImpl(user_repository, role_repository, user_role_repository)

# rota post, assign role to user
@router.post("/{user_id}/roles/{role_id}", status_code=204)
async def assign_role(
    user_id: int,
    role_id: int,
    service: UserRoleServiceImpl = Depends(get_user_role_service),
    current_user: User = Depends(get_current_user),
):
    try:
        await service.assign_role(user_id, role_id)
    except (UserNotFoundError, RoleNotFoundError):
        raise HTTPException(status_code=404, detail="usuário ou perfil não encontrado")
    except RoleAlreadyAssignedError:
        raise HTTPException(status_code=409, detail="usuário já possui esse perfil")


# rota delete, remove role from user
@router.delete("/{user_id}/roles/{role_id}", status_code=204)
async def remove_role(
    user_id: int,
    role_id: int,
    service: UserRoleServiceImpl = Depends(get_user_role_service),
    current_user: User = Depends(get_current_user),
):
    try:
        await service.remove_role(user_id, role_id)
    except RoleNotAssignedError:
        raise HTTPException(status_code=404, detail="usuário não possui esse perfil")


# rota get, list roles of a user
@router.get("/{user_id}/roles", response_model=RoleListResponse)
async def list_user_roles(
    user_id: int,
    service: UserRoleServiceImpl = Depends(get_user_role_service),
    current_user: User = Depends(get_current_user),
):
    roles = await service.list_roles(user_id)
    return RoleListResponse(roles=roles)
