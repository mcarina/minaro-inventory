from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.categorias.repository import SQLAlchemyCategoriaRepository
from app.categorias.service import CategoriaServiceImpl
from app.categorias.schemas import CategoriaCreate, CategoriaResponse, CategoriaListResponse, CategoriaUpdate
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(prefix="/categorias", tags=["categorias"])

def get_categoria_service(db: AsyncSession = Depends(get_db)) -> CategoriaServiceImpl:
    repository = SQLAlchemyCategoriaRepository(db)
    return CategoriaServiceImpl(repository)

# rota post, create categoria
@router.post("/", response_model=CategoriaResponse, status_code=201)
async def create_categoria(
    data: CategoriaCreate,
    service: CategoriaServiceImpl = Depends(get_categoria_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.create_categoria(data.nome, data.descricao)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

# rota get, get list of categorias
@router.get("/", response_model=CategoriaListResponse)
async def list_categorias(
    service: CategoriaServiceImpl = Depends(get_categoria_service),
    current_user: User = Depends(get_current_user),
):
    categorias = await service.list_categorias()
    return CategoriaListResponse(categorias=categorias)

# rota get by id
@router.get("/{categoria_id}", response_model=CategoriaResponse)
async def get_categoria(categoria_id: int, 
    service: CategoriaServiceImpl = Depends(get_categoria_service),
    current_user: User = Depends(get_current_user),
):
    categoria = await service.get_by_id(categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="categoria não encontrada")
    return categoria

# rota patch, update categoria
@router.patch("/{categoria_id}", response_model=CategoriaResponse)
async def update_categoria(
    categoria_id: int,
    data: CategoriaUpdate,
    service: CategoriaServiceImpl = Depends(get_categoria_service),
    current_user: User = Depends(get_current_user),
):
    try:
        categoria = await service.update_categoria(
            categoria_id,
            nome=data.nome,
            descricao=data.descricao,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if categoria is None:
        raise HTTPException(status_code=404, detail="categoria não encontrada")
    return categoria

# rota delete, delete user
@router.delete("/{categoria_id}", status_code=204)
async def delete_categoria(categoria_id: int, 
    service: CategoriaServiceImpl = Depends(get_categoria_service),
    current_user: User = Depends(get_current_user),
):
    success = await service.delete_categoria(categoria_id)
    if not success:
        raise HTTPException(status_code=404, detail="categoria não encontrada")