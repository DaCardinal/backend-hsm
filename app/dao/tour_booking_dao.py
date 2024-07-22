from uuid import UUID
from typing import Any, List, Union
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

# daos
from app.dao.base_dao import BaseDAO

# models
from app.models.tour_bookings import Tour

# utils
from app.utils.response import DAOResponse

# schema
from app.schema.tour import TourResponse, TourCreateSchema


class TourBookingDAO(BaseDAO[Tour]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = Tour
        self.primary_key = "tour_booking_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    # TODO:
    @override
    async def create(
        self, db_session: AsyncSession, obj_in: TourCreateSchema
    ) -> DAOResponse[TourResponse]:
        try:
            # extract base information
            transaction_info = self.extract_model_data(
                TourCreateSchema(**obj_in).model_dump(exclude=[""]), TourCreateSchema
            )
            new_transaction: Tour = await super().create(
                db_session=db_session, obj_in=transaction_info
            )

            # commit object to db session
            await self.commit_and_refresh(db_session, new_transaction)

            return DAOResponse[TourResponse](
                success=True, data=TourResponse.from_orm_model(new_transaction)
            )
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[TourResponse](success=False, error=f"Fatal {str(e)}")

    @override
    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> DAOResponse[List[TourResponse]]:
        result = await super().get_all(
            db_session=db_session, offset=offset, limit=limit
        )

        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[TourResponse]](
            success=True, data=[TourResponse.from_orm_model(r) for r in result]
        )

    @override
    async def get(
        self, db_session: AsyncSession, id: Union[UUID | Any | int]
    ) -> DAOResponse[TourResponse]:
        result: Tour = await super().get(db_session=db_session, id=id)

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[TourResponse](
            success=True, data=TourResponse.from_orm_model(result)
        )
