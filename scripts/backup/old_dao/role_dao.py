from typing import List
from sqlalchemy.sql import func
from sqlalchemy.future import select
from typing_extensions import override
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils.response import DAOResponse

# models
from app.models.role import Role
from app.models.permissions import Permissions

# daos
from app.dao.base_dao import BaseDAO
from app.dao.permission_dao import PermissionDAO

# schemas
from app.models.user_role import UserRoles
from app.schema.role import Role as RoleSchema, RoleResponse


class RoleDAO(BaseDAO[Role]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = Role
        self.primary_key = "role_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> DAOResponse[List[RoleResponse]]:
        result = await super().get_all(
            db_session=db_session, offset=offset, limit=limit
        )

        if not result:
            return DAOResponse(success=True, data=[])

        async with db_session as db:
            stmt = (
                select(Role.name, func.count(UserRoles.user_id).label("user_count"))
                .outerjoin(UserRoles, Role.role_id == UserRoles.role_id)
                .group_by(Role.name)
            )
            query_result = await db.execute(stmt)
            role_stats_results = query_result.all()

        return DAOResponse[List[RoleResponse]](
            success=True,
            data=[RoleResponse.from_orm_model(r) for r in result],
            meta={"role_stats": {name: count for name, count in role_stats_results}},
        )

    async def get_role_stats(self, db_session: AsyncSession):
        try:
            # TODO: Move this to base dao
            async with db_session as db:
                stmt = select(Role.name, func.count(Role.name).label("count")).group_by(
                    Role.name
                )
                query_result = await db.execute(stmt)

            # get results
            result = query_result.all()

            return DAOResponse(
                success=True, data={name: count for name, count in result}
            )
        except NoResultFound:
            return DAOResponse[str](success=False, error="Permission or Role not found")
        except Exception as e:
            return DAOResponse[str](success=False, error=str(e))

    async def add_role_permission(
        self, db_session: AsyncSession, role_alias: str, permission_alias: str
    ):
        permission_dao = PermissionDAO(Permissions)

        try:
            async with db_session as db:
                role: Role = await self.query(
                    db_session=db,
                    filters={"alias": role_alias},
                    single=True,
                    options=[selectinload(Role.permissions)],
                )
                permission: Permissions = await permission_dao.query(
                    db_session=db, filters={"alias": permission_alias}, single=True
                )

                if role is None or permission is None:
                    raise NoResultFound()

                if permission in role.permissions:
                    return DAOResponse[RoleSchema](
                        success=False,
                        error="Permission already exists for the role",
                        data=role.to_dict(),
                    )

                role.permissions.append(permission)
                await self.commit_and_refresh(db, role)

                return DAOResponse[RoleSchema](success=True, data=role.to_dict())
        except NoResultFound:
            return DAOResponse[str](success=False, error="Permission or Role not found")
        except Exception as e:
            return DAOResponse[str](success=False, error=str(e))
