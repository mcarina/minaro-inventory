from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.localizacoes.repository import SQLAlchemyLocalizacaoRepository
from app.localizacoes.service import LocalizacaoServiceImpl
from app.localizacoes.schemas import LocalizacaoCreate, LocalizacaoResponse, LocalizacaoListResponse, LocalizacaoUpdate
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(prefix="/localizacoes", tags=["localizacoes"])

def get_localizacao_service(db: AsyncSession = Depends(get_db)) -> LocalizacaoServiceImpl:
    repository = SQLAlchemyLocalizacaoRepository(db)
    return LocalizacaoServiceImpl(repository)

# rota post, create localizacao
@router.post("/", response_model=LocalizacaoResponse, status_code=201)
async def create_localizacao(
    data: LocalizacaoCreate,
    service: LocalizacaoServiceImpl = Depends(get_localizacao_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.create_localizacao(
            predio=data.predio,
            sala=data.sala,
            armario=data.armario,
            prateleira=data.prateleira,
            gaveta=data.gaveta
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

# rota get, get list of localizacoes
@router.get("/", response_model=LocalizacaoListResponse)
async def list_localizacoes(
    service: LocalizacaoServiceImpl = Depends(get_localizacao_service),
    current_user: User = Depends(get_current_user),
):
    localizacoes = await service.list_localizacoes()
    return LocalizacaoListResponse(localizacoes=localizacoes)

# rota get by id
@router.get("/{localizacao_id}", response_model=LocalizacaoResponse)
async def get_localizacao(localizacao_id: int, 
    service: LocalizacaoServiceImpl = Depends(get_localizacao_service),
    current_user: User = Depends(get_current_user),
):
    localizacao = await service.get_by_id(localizacao_id)
    if localizacao is None:
        raise HTTPException(status_code=404, detail="localizacao não encontrada")
    return localizacao

# rota patch, update localizacao
@router.patch("/{localizacao_id}", response_model=LocalizacaoResponse)
async def update_localizacao(
    localizacao_id: int,
    data: LocalizacaoUpdate,
    service: LocalizacaoServiceImpl = Depends(get_localizacao_service),
    current_user: User = Depends(get_current_user),
):
    try:
        localizacao = await service.update_localizacao(
            localizacao_id,
            predio=data.predio,
            sala=data.sala,
            armario=data.armario,
            prateleira=data.prateleira,
            gaveta=data.gaveta
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if localizacao is None:
        raise HTTPException(status_code=404, detail="localizacao não encontrada")
    return localizacao

# rota delete, delete localizacao
@router.delete("/{localizacao_id}", status_code=204)
async def delete_localizacao(localizacao_id: int, 
    service: LocalizacaoServiceImpl = Depends(get_localizacao_service),
    current_user: User = Depends(get_current_user),
):
    success = await service.delete_localizacao(localizacao_id)
    if not success:
        raise HTTPException(status_code=404, detail="localizacao não encontrada")