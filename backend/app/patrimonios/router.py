from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.patrimonios.repository import SQLAlchemyPatrimonioRepository
from app.patrimonios.service import PatrimonioServiceImpl
from app.patrimonios.schemas import PatrimonioCreate, PatrimonioResponse, PatrimonioListResponse, PatrimonioUpdate
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(prefix="/patrimonios", tags=["patrimonios"])

def get_patrimonio_service(db: AsyncSession = Depends(get_db)) -> PatrimonioServiceImpl:
    repository = SQLAlchemyPatrimonioRepository(db)
    return PatrimonioServiceImpl(repository)

# rota post, create patrimonio
@router.post("/", response_model=PatrimonioResponse, status_code=201)
async def create_patrimonio(
    data: PatrimonioCreate,
    service: PatrimonioServiceImpl = Depends(get_patrimonio_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.create_patrimonio(
            produto_id=data.produto_id,
            status=data.status,
            numero_patrimonio=data.numero_patrimonio,
            serial_number=data.serial_number
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=PatrimonioListResponse)
async def list_patrimonios(
    service: PatrimonioServiceImpl = Depends(get_patrimonio_service),
    current_user: User = Depends(get_current_user),
):
    patrimonios = await service.list_all()
    return PatrimonioListResponse(patrimonios=patrimonios)

@router.get("/{patrimonio_id}", response_model=PatrimonioResponse)
async def get_patrimonio(patrimonio_id: int, 
    service: PatrimonioServiceImpl = Depends(get_patrimonio_service),
    current_user: User = Depends(get_current_user),
):
    patrimonio = await service.get_by_id(patrimonio_id)
    if patrimonio is None:
        raise HTTPException(status_code=404, detail="patrimonio não encontrado")
    return patrimonio

@router.patch("/{patrimonio_id}", response_model=PatrimonioResponse)
async def update_patrimonio(
    patrimonio_id: int,
    data: PatrimonioUpdate,
    service: PatrimonioServiceImpl = Depends(get_patrimonio_service),
    current_user: User = Depends(get_current_user),
):
    try:
        patrimonio = await service.update(
            patrimonio_id,
            produto_id=data.produto_id,
            status=data.status,
            numero_patrimonio=data.numero_patrimonio,
            serial_number=data.serial_number
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if patrimonio is None:
        raise HTTPException(status_code=404, detail="patrimonio não encontrado")
    return patrimonio

@router.delete("/{patrimonio_id}", status_code=204)
async def delete_patrimonio(patrimonio_id: int,
    service: PatrimonioServiceImpl = Depends(get_patrimonio_service),
    current_user: User = Depends(get_current_user),
):
    success = await service.delete(patrimonio_id)
    if not success:
        raise HTTPException(status_code=404, detail="patrimonio não encontrado")