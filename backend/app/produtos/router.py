from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.produtos.repository import SQLAlchemyProdutoRepository
from app.produtos.service import ProdutoServiceImpl
from app.produtos.schemas import ProdutoCreate, ProdutoResponse, ProdutoListResponse, ProdutoUpdate
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(prefix="/produtos", tags=["produtos"])

def get_produto_service(db: AsyncSession = Depends(get_db)) -> ProdutoServiceImpl:
    repository = SQLAlchemyProdutoRepository(db)
    return ProdutoServiceImpl(repository)

# rota post, create produto
@router.post("/", response_model=ProdutoResponse, status_code=201)
async def create_produto(
    data: ProdutoCreate,
    service: ProdutoServiceImpl = Depends(get_produto_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.create_produto(
            nome=data.nome,
            descricao=data.descricao,
            categoria_id=data.categoria_id,
            marca_id=data.marca_id,
            codigo_interno=data.codigo_interno,
            codigo_barras=data.codigo_barras,
            modelo=data.modelo,
            localizacao_id=data.localizacao_id,
            estoque_minimo=data.estoque_minimo,
            ativo=data.ativo
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=ProdutoListResponse)
async def list_produtos(
    service: ProdutoServiceImpl = Depends(get_produto_service),
    current_user: User = Depends(get_current_user),
):
    produtos = await service.list_produtos()
    return ProdutoListResponse(produtos=produtos)

@router.get("/{produto_id}", response_model=ProdutoResponse)
async def get_produto(produto_id: int, 
    service: ProdutoServiceImpl = Depends(get_produto_service),
    current_user: User = Depends(get_current_user),
):
    produto = await service.get_by_id(produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="produto não encontrado")
    return produto

@router.patch("/{produto_id}", response_model=ProdutoResponse)
async def update_produto(
    produto_id: int,
    data: ProdutoUpdate,
    service: ProdutoServiceImpl = Depends(get_produto_service),
    current_user: User = Depends(get_current_user),
):
    try:
        produto = await service.update_produto(
            produto_id,
            nome=data.nome,
            descricao=data.descricao,
            categoria_id=data.categoria_id,
            marca_id=data.marca_id,
            codigo_interno=data.codigo_interno,
            codigo_barras=data.codigo_barras,
            modelo=data.modelo,
            localizacao_id=data.localizacao_id,
            estoque_minimo=data.estoque_minimo,
            ativo=data.ativo
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if produto is None:
        raise HTTPException(status_code=404, detail="produto não encontrado")
    return produto

@router.delete("/{produto_id}", status_code=204)
async def delete_produto(produto_id: int,
    service: ProdutoServiceImpl = Depends(get_produto_service),
    current_user: User = Depends(get_current_user),
):
    success = await service.delete_produto(produto_id)
    if not success:
        raise HTTPException(status_code=404, detail="produto não encontrado")