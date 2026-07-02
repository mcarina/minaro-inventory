from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.roles.models.role import Role

# INTERFACE REPOSITORY
class RoleRepository(ABC):
    @abstractmethod
    async def get_by_id(self, role_id: int) -> Role | None: ...

    @abstractmethod
    async def get_by_nome(self, nome: str) -> Role | None: ...

    @abstractmethod
    async def create(self, role: Role) -> Role: ...

    @abstractmethod
    async def list_all(self) -> list[Role]: ...

    @abstractmethod
    async def update(self, role: Role) -> Role: ...

    @abstractmethod
    async def delete(self, role: Role) -> None: ...

# REPOSITORY IMPLEMENTATION
class SQLAlchemyRoleRepository(RoleRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    # get role by id
    async def get_by_id(self, role_id: int) -> Role | None:
        result = await self.db.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

    # get role by nome
    async def get_by_nome(self, nome: str) -> Role | None:
        result = await self.db.execute(select(Role).where(Role.nome == nome))
        return result.scalar_one_or_none()

    # create role
    async def create(self, role: Role) -> Role:
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    # list all roles
    async def list_all(self) -> list[Role]:
        result = await self.db.execute(select(Role))
        return result.scalars().all()

    # update role
    async def update(self, role: Role) -> Role:
        await self.db.commit()
        await self.db.refresh(role)
        return role

    # delete role
    async def delete(self, role: Role) -> None:
        await self.db.delete(role)
        await self.db.commit()
