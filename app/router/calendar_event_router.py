from typing import List

from app.models import CalendarEvent
from app.router.base_router import BaseCRUDRouter
from app.dao.calendar_event_dao import CalendarEventDAO
from app.schema import CalendarEventSchema, CalendarEventCreateSchema, CalendarEventUpdateSchema

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
