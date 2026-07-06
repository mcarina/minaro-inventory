from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.estoques.repository import SQLAlchemyEstoqueRepository
from app.estoques.service import EstoqueServiceImpl
from app.estoques.schemas import EstoqueCreate, EstoqueResponse, EstoqueListResponse, EstoqueUpdate
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(prefix="/estoques", tags=["estoques"])

def get_estoque_service(db: AsyncSession = Depends(get_db)) -> EstoqueServiceImpl:
    repository = SQLAlchemyEstoqueRepository(db)
    return EstoqueServiceImpl(repository)

# rota post, create estoque
@router.post("/", response_model=EstoqueResponse, status_code=201)
async def create_estoque(
    data: EstoqueCreate,
    service: EstoqueServiceImpl = Depends(get_estoque_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.create_estoque(
            produto_id=data.produto_id,
            quantidade=data.quantidade
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=EstoqueListResponse)
async def list_estoques(
    service: EstoqueServiceImpl = Depends(get_estoque_service),
    current_user: User = Depends(get_current_user),
):
    estoques = await service.list_all()
    return EstoqueListResponse(estoques=estoques)

@router.get("/{estoque_id}", response_model=EstoqueResponse)
async def get_estoque(estoque_id: int, 
    service: EstoqueServiceImpl = Depends(get_estoque_service),
    current_user: User = Depends(get_current_user),
):
    estoque = await service.get_by_id(estoque_id)
    if estoque is None:
        raise HTTPException(status_code=404, detail="estoque não encontrado")
    return estoque

@router.patch("/{estoque_id}", response_model=EstoqueResponse)
async def update_estoque(
    estoque_id: int,
    data: EstoqueUpdate,
    service: EstoqueServiceImpl = Depends(get_estoque_service),
    current_user: User = Depends(get_current_user),
):
    try:
        estoque = await service.update(
            estoque_id,
            produto_id=data.produto_id,
            quantidade=data.quantidade
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if estoque is None:
        raise HTTPException(status_code=404, detail="estoque não encontrado")
    return estoque

@router.delete("/{estoque_id}", status_code=204)
async def delete_estoque(estoque_id: int,
    service: EstoqueServiceImpl = Depends(get_estoque_service),
    current_user: User = Depends(get_current_user),
):
    success = await service.delete(estoque_id)
    if not success:
        raise HTTPException(status_code=404, detail="estoque não encontrado")