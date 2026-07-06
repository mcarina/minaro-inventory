from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.emprestimo.repository import SQLAlchemyEmprestimoRepository
from app.emprestimo.service import EmprestimoServiceImpl
from app.emprestimo.schemas import EmprestimoCreate, EmprestimoResponse, EmprestimoListResponse, EmprestimoUpdate
from app.auth.dependencies import get_current_user
from app.users.models.user import User

router = APIRouter(prefix="/emprestimos", tags=["emprestimos"])

def get_emprestimo_service(db: AsyncSession = Depends(get_db)) -> EmprestimoServiceImpl:
    repository = SQLAlchemyEmprestimoRepository(db)
    return EmprestimoServiceImpl(repository)

# rota post, create emprestimo
@router.post("/", response_model=EmprestimoResponse, status_code=201)
async def create_emprestimo(
    data: EmprestimoCreate,
    service: EmprestimoServiceImpl = Depends(get_emprestimo_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.create_emprestimo(
            usuario_responsavel_id=data.usuario_responsavel_id,
            setor_id=data.setor_id,
            data_saida=data.data_saida,
            data_prevista=data.data_prevista,
            data_devolucao=data.data_devolucao,
            status=data.status
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=EmprestimoListResponse)
async def list_emprestimos(
    service: EmprestimoServiceImpl = Depends(get_emprestimo_service),
    current_user: User = Depends(get_current_user),
):
    emprestimos = await service.list_all()
    return EmprestimoListResponse(emprestimos=emprestimos)

@router.get("/{emprestimo_id}", response_model=PatrimonioResponse)
async def get_patrimonio(patrimonio_id: int, 
    service: PatrimonioServiceImpl = Depends(get_patrimonio_service),
    current_user: User = Depends(get_current_user),
):
    patrimonio = await service.get_by_id(patrimonio_id)
    if patrimonio is None:
        raise HTTPException(status_code=404, detail="patrimonio não encontrado")
    return patrimonio

@router.patch("/{emprestimo_id}", response_model=EmprestimoResponse)
async def update_emprestimo(
    emprestimo_id: int,
    data: EmprestimoUpdate,
    service: EmprestimoServiceImpl = Depends(get_emprestimo_service),
    current_user: User = Depends(get_current_user),
):
    try:
        emprestimo = await service.update(
            emprestimo_id,
            usuario_responsavel_id=data.usuario_responsavel_id,
            setor_id=data.setor_id,
            data_saida=data.data_saida,
            data_prevista=data.data_prevista,
            data_devolucao=data.data_devolucao,
            status=data.status
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if emprestimo  is None:
        raise HTTPException(status_code=404, detail="emprestimo não encontrado")
    return emprestimo

@router.delete("/{emprestimo_id}", status_code=204)
async def delete_emprestimo(emprestimo_id: int,
    service: EmprestimoServiceImpl = Depends(get_emprestimo_service),
    current_user: User = Depends(get_current_user),
):
    success = await service.delete(emprestimo_id)
    if not success:
        raise HTTPException(status_code=404, detail="emprestimo não encontrado")