from abc import ABC, abstractmethod
from app.roles.models.role import Role
from app.roles.repository import RoleRepository

# INTERFACE Service
class RoleService(ABC):
    @abstractmethod
    async def get_by_id(self, role_id: int) -> Role | None: ...

    @abstractmethod
    async def list_roles(self) -> list[Role]: ...

    @abstractmethod
    async def create_role(self, nome: str) -> Role: ...

    @abstractmethod
    async def update_role(self, role_id: int, nome: str | None = None) -> Role | None: ...

    @abstractmethod
    async def delete_role(self, role_id: int) -> bool: ...

# Service Implementation
class RoleServiceImpl(RoleService):
    def __init__(self, repository: RoleRepository):
        self.repository = repository

    # get role by id service
    async def get_by_id(self, role_id: int) -> Role | None:
        return await self.repository.get_by_id(role_id)

    # list all roles service
    async def list_roles(self) -> list[Role]:
        return await self.repository.list_all()

    # create role service
    async def create_role(self, nome: str) -> Role:
        existing_role = await self.repository.get_by_nome(nome)
        if existing_role is not None:
            raise ValueError("perfil já existe")

        role = Role(nome=nome)
        return await self.repository.create(role)

    # update role service
    async def update_role(self, role_id: int, nome: str | None = None) -> Role | None:
        role = await self.repository.get_by_id(role_id)
        if role is None:
            return None

        if nome is not None:
            existing_role = await self.repository.get_by_nome(nome)
            if existing_role is not None and existing_role.id != role_id:
                raise ValueError("perfil já existe")
            role.nome = nome

        return await self.repository.update(role)

    # delete role service
    async def delete_role(self, role_id: int) -> bool:
        role = await self.repository.get_by_id(role_id)
        if role is None:
            return False

        await self.repository.delete(role)
        return True
