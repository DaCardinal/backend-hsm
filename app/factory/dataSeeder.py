from typing import List, Union
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dbCrud import DBOperations
from app.db.dbManager import DBManager
from app.factory.dataFactory import DataFactory

class DataSeeder():
    def __init__(self, data_factory: Union[DataFactory, List[DataFactory]]):
        self.data_factory = data_factory
        self.db_manager = DBManager()

    async def seed_data(self):
        async with self.db_manager.db_module.Session() as session:
            if isinstance(self.data_factory, list):
                for data_factory_item in self.data_factory:
                    await self._process_data_factory(session, data_factory_item)
            else:
                await self._process_data_factory(session, self.data_factory)

    async def _process_data_factory(self, session: AsyncSession, data_factory: DataFactory):
        query_key, data = data_factory.create_data()
        data : List[dict] = data
        db_crud = DBOperations(data_factory.model)

        for item_data in data:
            item = await db_crud.query(
                db_session=session,
                filters={query_key: item_data.get(query_key)},
                single=True
            )

            if not item:
                await db_crud.create(db_session=session, obj_in=item_data)
