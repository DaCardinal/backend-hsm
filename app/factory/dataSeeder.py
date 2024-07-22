from importlib import import_module
from typing import List, Union
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dbCrud import DBOperations
from app.db.dbManager import DBManager
from app.factory.dataFactory import DataFactory
# from app.dao.role_dao import RoleDAO


class DataSeeder:
    def __init__(self, data_factory: Union[DataFactory, List[DataFactory]]):
        self.data_factory = data_factory
        self.db_manager = DBManager()

    async def seed_data(self):
        async with self.db_manager.db_module.Session() as session:
            if isinstance(self.data_factory, list):
                for data_factory_item in self.data_factory:
                    if data_factory_item.model.__name__ == "RolePermissions":
                        await self._process_role_permissions(session, data_factory_item)
                    else:
                        await self._process_data_factory(session, data_factory_item)

            else:
                await self._process_data_factory(session, self.data_factory)

    async def _process_data_factory(
        self, session: AsyncSession, data_factory: DataFactory
    ):
        query_key, data = data_factory.create_data()
        data: List[dict] = data
        db_crud = DBOperations(data_factory.model)

        for item_data in data:
            item = await db_crud.query(
                db_session=session,
                filters={query_key: item_data.get(query_key)},
                single=True,
            )

            if not item:
                user = await db_crud.create(db_session=session, obj_in=item_data)

                if data_factory.model.__name__ == "User" and user:
                    role = user.email.split("@")[0]

                    # user dao model
                    models_module = import_module("app.dao.user_dao")
                    UserDAO = getattr(models_module, "UserDAO")

                    # user dao instance
                    db_crud_dao = UserDAO(data_factory.model)
                    await db_crud_dao.add_user_role(
                        db_session=session, user_id=user.user_id, role_alias=role
                    )

    async def _process_role_permissions(
        self, session: AsyncSession, data_factory: DataFactory
    ):
        query_key, data = data_factory.create_data()

        # role model
        role_models_module = import_module("app.models")
        RoleObject = getattr(role_models_module, "Role")

        # role dao model
        models_module = import_module("app.dao.role_dao")
        RoleDAO = getattr(models_module, "RoleDAO")

        # role dao instance
        db_crud_dao = RoleDAO(RoleObject)

        for role_permission in data:
            role_name = role_permission["name"]
            role_permissions = role_permission["permissions"]

            for permission in role_permissions:
                await db_crud_dao.add_role_permission(
                    db_session=session,
                    role_alias=role_name,
                    permission_alias=permission["alias"],
                )
