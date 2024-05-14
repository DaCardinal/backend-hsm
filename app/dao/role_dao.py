from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import NoResultFound
from typing import Type

# local imports
from app.dao.base_dao import BaseDAO
from app.dao.permission_dao import PermissionDAO
from app.utils.response import DAOResponse
from app.models import Role, Permissions
from app.schema import Role as RoleSchema

class RoleDAO(BaseDAO[Role]):
    def __init__(self, model: Type[Role], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        super().__init__(model, load_parent_relationships, load_child_relationships, excludes=excludes)
        self.primary_key = "role_id"
    
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