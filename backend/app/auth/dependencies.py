import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.users.repository import SQLAlchemyUserRepository
from app.users.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="token inválido ou expirado")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="token inválido")

    repository = SQLAlchemyUserRepository(db)
    user = await repository.get_by_id(int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="usuário não encontrado")

    return user
