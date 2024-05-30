from typing import List

from app.models import CalendarEvent
from app.dao.calendar_event_dao import CalendarEventDAO
from app.schema import CalendarEventSchema, CalendarEventCreateSchema, CalendarEventUpdateSchema
from app.router.base_router import BaseCRUDRouter

class CalendarEventRouter(BaseCRUDRouter):

    def __init__(self, dao: CalendarEventDAO = CalendarEventDAO(CalendarEvent, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
       
        self.dao = dao
        CalendarEventSchema["create_schema"] = CalendarEventCreateSchema
        CalendarEventSchema["update_schema"] = CalendarEventUpdateSchema
        super().__init__(dao=dao, schemas=CalendarEventSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
