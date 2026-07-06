from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.movimentacoes.repository import SQLAlchemyMovimentacaoRepository
from app.movimentacoes.service import MovimentacaoServiceImpl
from app.movimentacoes.schemas import MovimentacaoCreate, MovimentacaoResponse, MovimentacaoListResponse, MovimentacaoUpdate
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(prefix="/movimentacoes", tags=["movimentacoes"])

def get_movimentacao_service(db: AsyncSession = Depends(get_db)) -> MovimentacaoServiceImpl:
    repository = SQLAlchemyMovimentacaoRepository(db)
    return MovimentacaoServiceImpl(repository)

# rota post, create movimentacao
@router.post("/", response_model=MovimentacaoResponse, status_code=201)
async def create_movimentacao(
    data: MovimentacaoCreate,
    service: MovimentacaoServiceImpl = Depends(get_movimentacao_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.create_movimentacao(
            produto_id=data.produto_id,
            user_id=data.user_id,
            tipo=data.tipo,
            quantidade=data.quantidade,
            data=data.data,
            motivo=data.motivo
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=MovimentacaoListResponse)
async def list_movimentacoes(
    service: MovimentacaoServiceImpl = Depends(get_movimentacao_service),
    current_user: User = Depends(get_current_user),
):
    movimentacoes = await service.list_all()
    return MovimentacaoListResponse(movimentacoes=movimentacoes)

@router.get("/{movimentacao_id}", response_model=MovimentacaoResponse)
async def get_movimentacao(movimentacao_id: int, 
    service: MovimentacaoServiceImpl = Depends(get_movimentacao_service),
    current_user: User = Depends(get_current_user),
):
    movimentacao = await service.get_by_id(movimentacao_id)
    if movimentacao is None:
        raise HTTPException(status_code=404, detail="movimentacao não encontrada")
    return movimentacao

@router.patch("/{movimentacao_id}", response_model=MovimentacaoResponse)
async def update_movimentacao(
    movimentacao_id: int,
    data: MovimentacaoUpdate,
    service: MovimentacaoServiceImpl = Depends(get_movimentacao_service),
    current_user: User = Depends(get_current_user),
):
    try:
        movimentacao = await service.update(
            movimentacao_id,
            produto_id=data.produto_id,
            user_id=data.user_id,
            tipo=data.tipo,
            quantidade=data.quantidade,
            data=data.data,
            motivo=data.motivo
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if movimentacao is None:
        raise HTTPException(status_code=404, detail="movimentacao não encontrada")
    return movimentacao

@router.delete("/{movimentacao_id}", status_code=204)
async def delete_movimentacao(movimentacao_id: int,
    service: MovimentacaoServiceImpl = Depends(get_movimentacao_service),
    current_user: User = Depends(get_current_user),
):
    success = await service.delete(movimentacao_id)
    if not success:
        raise HTTPException(status_code=404, detail="movimentacao não encontrada")