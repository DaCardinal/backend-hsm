from typing import List

from app.router.base_router import BaseCRUDRouter

# daos
from app.dao.calendar_event_dao import CalendarEventDAO

# schemas
from app.schema.schemas import CalendarEventSchema
from app.schema.calendar_event import CalendarEventCreateSchema, CalendarEventUpdateSchema

class CalendarEventRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):

        # initialize router dao
        CalendarEventSchema["create_schema"] = CalendarEventCreateSchema
        CalendarEventSchema["update_schema"] = CalendarEventUpdateSchema
        self.dao: CalendarEventDAO = CalendarEventDAO(nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=CalendarEventSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
