from typing import List

from app.models import Tour
from app.dao.tour_booking_dao import TourBookingDAO
from app.schema import TourBookingSchema
from app.router.base_router import BaseCRUDRouter

class TourBookingRouter(BaseCRUDRouter):

    def __init__(self, dao: TourBookingDAO = TourBookingDAO(Tour, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=TourBookingSchema, prefix=prefix, tags=tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        pass
