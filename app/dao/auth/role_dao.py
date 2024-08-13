from sqlalchemy.sql import func
from sqlalchemy.future import select
from typing import Dict, List
from typing_extensions import override
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils.response import DAOResponse

# models
from app.models.role import Role
from app.models.user_role import UserRoles
from app.models.permissions import Permissions

# daos
from app.dao.resources.base_dao import BaseDAO
from app.dao.auth.permission_dao import PermissionDAO

# schemas
from app.schema.role import RoleResponse


class RoleDAO(BaseDAO[Role]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = Role
        self.primary_key = "role_id"

        self.permission_dao = PermissionDAO()
        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def get_all(
        self, db_session: AsyncSession, offset: int = 0, limit: int = 100
    ) -> DAOResponse[List[RoleResponse]]:
        """
        Retrieve all roles with pagination, including role statistics such as user count per role.
        """
        roles = await super().get_all(db_session=db_session, offset=offset, limit=limit)

        if not roles:
            return DAOResponse(success=True, data=[])

        role_stats = await self.fetch_role_stats(db_session)

        return DAOResponse[List[RoleResponse]](
            success=True,
            data=[RoleResponse.from_orm_model(role) for role in roles],
            meta={"role_stats": role_stats},
        )

    async def fetch_role_stats(self, db_session: AsyncSession) -> Dict[str, int]:
        """
        Fetch statistics for roles, such as the number of users associated with each role.
        """
        async with db_session as db:
            stmt = (
                select(Role.name, func.count(UserRoles.user_id).label("user_count"))
                .outerjoin(UserRoles, Role.role_id == UserRoles.role_id)
                .group_by(Role.name)
            )
            query_result = await db.execute(stmt)
            role_stats_results = query_result.all()

        return {name: count for name, count in role_stats_results}

    async def add_role_permission(
        self, db_session: AsyncSession, role_alias: str, permission_alias: str
    ) -> DAOResponse:
        """
        Add a permission to a role, ensuring the permission doesn't already exist for the role.
        """
        try:
            role, permission = await self.fetch_role_and_permission(
                db_session, role_alias, permission_alias
            )

            if permission in role.permissions:
                return DAOResponse(
                    success=False,
                    error="Permission already exists for the role",
                    data=role.to_dict(),
                )

            role.permissions.append(permission)
            await self.commit_and_refresh(db_session, role)

            return DAOResponse(success=True, data=role.to_dict())

        except NoResultFound:
            return DAOResponse(success=False, error="Permission or Role not found")
        except Exception as e:
            return DAOResponse(success=False, error=str(e))

    async def fetch_role_and_permission(
        self, db_session: AsyncSession, role_alias: str, permission_alias: str
    ) -> tuple[Role, Permissions]:
        """
        Fetch role and permission objects based on their aliases.
        """
        role = await self.query(
            db_session=db_session,
            filters={"alias": role_alias},
            single=True,
            options=[selectinload(Role.permissions)],
        )

        permission = await self.permission_dao.query(
            db_session=db_session, filters={"alias": permission_alias}, single=True
        )

        if role is None or permission is None:
            raise NoResultFound("Role or permission not found!")

        return role, permission
