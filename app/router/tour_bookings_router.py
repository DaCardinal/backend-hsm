from typing import List

from app.schema.schemas import TourBookingSchema
from app.router.base_router import BaseCRUDRouter
from app.dao.tour_booking_dao import TourBookingDAO

class TourBookingRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao : TourBookingDAO = TourBookingDAO(nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[''])

        super().__init__(dao=self.dao, schemas=TourBookingSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):
        pass
