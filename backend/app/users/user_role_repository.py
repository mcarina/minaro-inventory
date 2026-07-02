from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models.user_role import UserRole
from app.roles.models.role import Role

# Repository interface
class UserRoleRepository(ABC):
    @abstractmethod
    async def get(self, user_id: int, role_id: int) -> UserRole | None: ...

    @abstractmethod
    async def create(self, user_role: UserRole) -> UserRole: ...

    @abstractmethod
    async def delete(self, user_role: UserRole) -> None: ...

    @abstractmethod
    async def list_roles_by_user(self, user_id: int) -> list[Role]: ...

# implementation of the repository
class SQLAlchemyUserRoleRepository(UserRoleRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, user_id: int, role_id: int) -> UserRole | None:
        result = await self.db.execute(
            select(UserRole).where(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, user_role: UserRole) -> UserRole:
        self.db.add(user_role)
        await self.db.commit()
        await self.db.refresh(user_role)
        return user_role

    async def delete(self, user_role: UserRole) -> None:
        await self.db.delete(user_role)
        await self.db.commit()

    async def list_roles_by_user(self, user_id: int) -> list[Role]:
        result = await self.db.execute(
            select(Role).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user_id)
        )
        return result.scalars().all()
