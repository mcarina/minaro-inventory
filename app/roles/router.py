from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.roles.repository import SQLAlchemyRoleRepository
from app.roles.service import RoleServiceImpl
from app.roles.schemas import RoleCreate, RoleResponse, RoleListResponse, RoleUpdate

router = APIRouter(prefix="/roles", tags=["roles"])

def get_role_service(db: AsyncSession = Depends(get_db)) -> RoleServiceImpl:
    repository = SQLAlchemyRoleRepository(db)
    return RoleServiceImpl(repository)

# rota post, create role
@router.post("/", response_model=RoleResponse, status_code=201)
async def create_role(
    data: RoleCreate,
    service: RoleServiceImpl = Depends(get_role_service),
):
    try:
        return await service.create_role(data.nome)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

# rota get, list roles
@router.get("/", response_model=RoleListResponse)
async def list_roles(
    service: RoleServiceImpl = Depends(get_role_service),
):
    roles = await service.list_roles()
    return RoleListResponse(roles=roles)

# rota get by id
@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int, service: RoleServiceImpl = Depends(get_role_service)):
    role = await service.get_by_id(role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="perfil não encontrado")
    return role

# rota patch, update role
@router.patch("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    data: RoleUpdate,
    service: RoleServiceImpl = Depends(get_role_service),
):
    try:
        role = await service.update_role(
            role_id,
            nome=data.nome,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if role is None:
        raise HTTPException(status_code=404, detail="perfil não encontrado")

    return role

# rota delete, delete role
@router.delete("/{role_id}", status_code=204)
async def delete_role(
    role_id: int,
    service: RoleServiceImpl = Depends(get_role_service),
):
    success = await service.delete_role(role_id)
    if not success:
        raise HTTPException(status_code=404, detail="perfil não encontrado")
