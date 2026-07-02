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

    @abstractmethod
    async def update_user(
        self,
        user_id: int,
        nome: str | None = None,
        email: str | None = None,
        password: str | None = None,
        ativo: bool | None = None,
    ) -> User | None: ...

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool: ...

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

    # get user by email service
    async def get_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_email(email)

    # list all users service
    async def list_users(self) -> list[User]:
        return await self.repository.list_all()

    # update user service
    async def update_user(
        self,
        user_id: int,
        nome: str | None = None,
        email: str | None = None,
        password: str | None = None,
        ativo: bool | None = None,
    ) -> User | None:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            return None

        if nome is not None:
            user.nome = nome
        if email is not None:
            existing = await self.repository.get_by_email(email)
            if existing is not None and existing.id != user_id:
                raise ValueError("email já cadastrado")
            user.email = email
        if password is not None:
            user.senha_hash = hash_password(password)
        if ativo is not None:
            user.ativo = ativo

        return await self.repository.update(user)

    # delete user service
    async def delete_user(self, user_id: int) -> bool:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            return False

        await self.repository.delete(user)
        return True