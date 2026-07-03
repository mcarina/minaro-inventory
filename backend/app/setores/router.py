from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.setores.repository import SQLAlchemySetorRepository
from app.setores.service import SetorServiceImpl
from app.setores.schemas import SetorCreate, SetorResponse, SetorListResponse, SetorUpdate
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(prefix="/setores", tags=["setores"])

def get_setor_service(db: AsyncSession = Depends(get_db)) -> SetorServiceImpl:
    repository = SQLAlchemySetorRepository(db)
    return SetorServiceImpl(repository)

# rota post, create setor
@router.post("/", response_model=SetorResponse, status_code=201)
async def create_setor(
    data: SetorCreate,
    service: SetorServiceImpl = Depends(get_setor_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.create_setor(
            nome=data.nome
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

# rota get, get list of setores
@router.get("/", response_model=SetorListResponse)
async def list_setores(
    service: SetorServiceImpl = Depends(get_setor_service),
    current_user: User = Depends(get_current_user),
):
    setores = await service.list_setores()
    return SetorListResponse(setores=setores)
    
# rota get by id
@router.get("/{setor_id}", response_model=SetorResponse)
async def get_setor(setor_id: int, 
    service: SetorServiceImpl = Depends(get_setor_service),
    current_user: User = Depends(get_current_user),
):
    setor = await service.get_by_id(setor_id)
    if setor is None:
        raise HTTPException(status_code=404, detail="setor não encontrado")
    return setor

# rota patch, update setor
@router.patch("/{setor_id}", response_model=SetorResponse)
async def update_setor(
    setor_id: int,
    data: SetorUpdate,
    service: SetorServiceImpl = Depends(get_setor_service),
    current_user: User = Depends(get_current_user),
):
    try:
        setor = await service.update_setor(
            setor_id,
            nome=data.nome
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if setor is None:
        raise HTTPException(status_code=404, detail="setor não encontrado")
    return setor

# rota delete, delete setor
@router.delete("/{setor_id}", status_code=204)
async def delete_setor(setor_id: int, 
    service: SetorServiceImpl = Depends(get_setor_service),
    current_user: User = Depends(get_current_user),
):
    success = await service.delete_setor(setor_id)
    if not success:
        raise HTTPException(status_code=404, detail="setor não encontrado")
    