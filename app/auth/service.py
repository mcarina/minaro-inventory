from abc import ABC, abstractmethod
from app.users.service import UserService

class AuthService(ABC):
    @abstractmethod
    async def login(self, email: str, password: str) -> str: ...

class AuthServiceImpl(AuthService):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def login(self, email: str, password: str) -> str:
        user = await self.user_service.get_by_email(email)
        if user is None:
            raise ValueError("Usuário não encontrado")

        from app.core.security import verify_password, create_access_token

        if not verify_password(password, user.senha_hash):
            raise ValueError("Senha incorreta")

        access_token = create_access_token({"sub": str(user.id)})
        return access_token