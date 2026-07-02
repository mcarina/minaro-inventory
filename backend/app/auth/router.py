from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.users.repository import SQLAlchemyUserRepository
from app.users.service import UserServiceImpl
from app.auth.service import AuthServiceImpl
from app.auth.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthServiceImpl:
    repository = SQLAlchemyUserRepository(db)
    user_service = UserServiceImpl(repository)
    return AuthServiceImpl(user_service)

# login endpoint
@router.post("/", response_model=TokenResponse)
async def login(request: LoginRequest, auth_service: AuthServiceImpl = Depends(get_auth_service )):
    try:
        access_token = await auth_service.login(request.email, request.password)
        return TokenResponse(access_token=access_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))