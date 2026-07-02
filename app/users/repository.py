from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models.user import User
from abc import ABC, abstractmethod

# INTERFACE REPOSITORY
class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def list_all(self) -> list[User]: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get user by id
    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
        
    # get user by email
    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    # create user
    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # list all users
    async def list_all(self) -> list[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()