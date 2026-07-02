from abc import ABC, abstractmethod
from app.users.models.user import User
from app.users.repository import UserRepository
from app.core.security import hash_password

# Service Interface
class UserService(ABC):
    @abstractmethod
    async def create_user(self, nome: str, email: str, password: str) -> User: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def list_users(self) -> list[User]: ...

# Service Implementation
class UserServiceImpl(UserService):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    # create user service
    async def create_user(self, nome: str, email: str, password: str) -> User:
        existing = await self.repository.get_by_email(email)
        if existing is not None:
            raise ValueError("email já cadastrado")

        user = User(
            nome=nome,
            email=email,
            senha_hash=hash_password(password),
        )
        return await self.repository.create(user)

    # get user by id service
    async def get_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_by_id(user_id)

    # list all users service
    async def list_users(self) -> list[User]:
        return await self.repository.list_all()