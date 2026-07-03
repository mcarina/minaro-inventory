from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.marcas.repository import SQLAlchemyMarcaRepository
from app.marcas.service import MarcaServiceImpl
from app.marcas.schemas import MarcaCreate, MarcaResponse, MarcaListResponse, MarcaUpdate
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(prefix="/marcas", tags=["marcas"])

def get_marca_service(db: AsyncSession = Depends(get_db)) -> MarcaServiceImpl:
    repository = SQLAlchemyMarcaRepository(db)
    return MarcaServiceImpl(repository)

# rota post, create marca
@router.post("/", response_model=MarcaResponse, status_code=201)
async def create_marca(
    data: MarcaCreate,
    service: MarcaServiceImpl = Depends(get_marca_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.create_marca(
            nome=data.nome
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

# rota get, get list of marcas
@router.get("/", response_model=MarcaListResponse)
async def list_marcas(
    service: MarcaServiceImpl = Depends(get_marca_service),
    current_user: User = Depends(get_current_user),
):
    marcas = await service.list_marcas()
    return MarcaListResponse(marcas=marcas)

# rota get by id
@router.get("/{marca_id}", response_model=MarcaResponse)
async def get_marca(marca_id: int, 
    service: MarcaServiceImpl = Depends(get_marca_service),
    current_user: User = Depends(get_current_user),
):
    marca = await service.get_by_id(marca_id)
    if marca is None:
        raise HTTPException(status_code=404, detail="marca não encontrada")
    return marca

# rota patch, update marca
@router.patch("/{marca_id}", response_model=MarcaResponse)
async def update_marca(
    marca_id: int,
    data: MarcaUpdate,
    service: MarcaServiceImpl = Depends(get_marca_service),
    current_user: User = Depends(get_current_user),
):
    try:
        marca = await service.update_marca(
            marca_id,
            nome=data.nome
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if marca is None:
        raise HTTPException(status_code=404, detail="marca não encontrada")
    return marca

# rota delete, delete marca
@router.delete("/{marca_id}", status_code=204)
async def delete_marca(marca_id: int, 
    service: MarcaServiceImpl = Depends(get_marca_service),
    current_user: User = Depends(get_current_user),
):
    success = await service.delete_marca(marca_id)
    if not success:
        raise HTTPException(status_code=404, detail="marca não encontrada")
    