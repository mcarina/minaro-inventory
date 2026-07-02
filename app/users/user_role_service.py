from abc import ABC, abstractmethod
from app.users.models.user import User
from app.roles.models.role import Role
from app.users.models.user_role import UserRole
from app.users.repository import UserRepository
from app.roles.repository import RoleRepository
from app.users.user_role_repository import UserRoleRepository

# exceções customizadas
class UserNotFoundError(Exception):
    pass


class RoleNotFoundError(Exception):
    pass


class RoleAlreadyAssignedError(Exception):
    pass


class RoleNotAssignedError(Exception):
    pass


# Service interface
class UserRoleService(ABC):
    @abstractmethod
    async def assign_role(self, user_id: int, role_id: int) -> UserRole: ...

    @abstractmethod
    async def remove_role(self, user_id: int, role_id: int) -> None: ...

    @abstractmethod
    async def list_roles(self, user_id: int) -> list[Role]: ...


# Service implementation
class UserRoleServiceImpl(UserRoleService):
    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        user_role_repository: UserRoleRepository,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.user_role_repository = user_role_repository

    async def assign_role(self, user_id: int, role_id: int) -> UserRole:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        role = await self.role_repository.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundError()

        existing = await self.user_role_repository.get(user_id, role_id)
        if existing is not None:
            raise RoleAlreadyAssignedError()

        user_role = UserRole(user_id=user_id, role_id=role_id)
        return await self.user_role_repository.create(user_role)

    async def remove_role(self, user_id: int, role_id: int) -> None:
        existing = await self.user_role_repository.get(user_id, role_id)
        if existing is None:
            raise RoleNotAssignedError()

        await self.user_role_repository.delete(existing)

    async def list_roles(self, user_id: int) -> list[Role]:
        return await self.user_role_repository.list_roles_by_user(user_id)
