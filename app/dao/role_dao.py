from sqlalchemy.sql import func
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# local imports
from app.dao.base_dao import BaseDAO
from app.dao.permission_dao import PermissionDAO
from app.utils.response import DAOResponse
from app.models import Role, Permissions
from app.schema import Role as RoleSchema

class RoleDAO(BaseDAO[Role]):
    def __init__(self, excludes = [], nesting_degree : str = BaseDAO.NO_NESTED_CHILD):
        self.model = Role
        self.primary_key = "role_id"

        super().__init__(self.model, nesting_degree = nesting_degree, excludes=excludes)
    
    async def get_role_stats(self, db_session: AsyncSession):
        try:
            # TODO: Move this to base dao
            async with db_session as db:
                stmt = select(Role.name, func.count(Role.name).label('count')).group_by(Role.name)
                query_result = await db_session.execute(stmt)
            
            # get results
            result = query_result.all()

            return DAOResponse(success=True, data={name: count for name, count in result})
        except NoResultFound as e:
            return DAOResponse[str](success=False, error="Permission or Role not found")
        except Exception as e:
            return DAOResponse[str](success=False, error=str(e))
        
    async def add_role_permission(self, db_session: AsyncSession, role_alias: str, permission_alias: str):
        permission_dao = PermissionDAO(Permissions)

        try:
            async with db_session as db:
                role: Role = await self.query(db_session=db, filters={f"alias": role_alias},single=True,options=[selectinload(Role.permissions)])
                permission: Permissions = await permission_dao.query(db_session=db, filters={f"alias": permission_alias}, single=True)

                if role is None or permission is None:
                    raise NoResultFound()
        
                if permission in role.permissions:
                    return DAOResponse[RoleSchema](success=False, error="Permission already exists for the role", data=role.to_dict())
                
                role.permissions.append(permission)
                await self.commit_and_refresh(db, role)

                return DAOResponse[RoleSchema](success=True, data=role.to_dict())
        except NoResultFound as e:
            return DAOResponse[str](success=False, error="Permission or Role not found")
        except Exception as e:
            return DAOResponse[str](success=False, error=str(e))