from uuid import UUID
from typing import Any, List, Union
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils.response import DAOResponse

# models
from app.models.calendar_event import CalendarEvent

# daos
from app.dao.resources.base_dao import BaseDAO

# schemas
from app.schema.enums import EventType
from app.schema.calendar_event import (
    CalendarEventBase,
    CalendarEventResponse,
    CalendarEventCreateSchema,
    CalendarEventUpdateSchema,
)


class CalendarEventDAO(BaseDAO[CalendarEvent]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = CalendarEvent
        self.primary_key = "event_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: CalendarEventCreateSchema
    ) -> DAOResponse[CalendarEventResponse]:
        try:
            # extract base information
            calendar_event_info = self.extract_model_data(obj_in, CalendarEventBase)
            calendar_event_info["event_type"] = EventType(
                calendar_event_info["event_type"]
            )
            new_calendar_event: CalendarEvent = await super().create(
                db_session=db_session, obj_in={**calendar_event_info}
            )

            # commit object to db session
            await self.commit_and_refresh(db_session, new_calendar_event)

            return DAOResponse[CalendarEventResponse](
                success=True,
                data=CalendarEventResponse.from_orm_model(new_calendar_event),
            )
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[CalendarEventResponse](
                success=False, error=f"Fatal {str(e)}"
            )

    @override
    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> DAOResponse[List[CalendarEventResponse]]:
        result = await super().get_all(
            db_session=db_session, offset=offset, limit=limit
        )

        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[CalendarEventResponse]](
            success=True, data=[CalendarEventResponse.from_orm_model(r) for r in result]
        )

    @override
    async def get(
        self, db_session: AsyncSession, id: Union[UUID | Any | int]
    ) -> DAOResponse[CalendarEventResponse]:
        result: CalendarEvent = await super().get(db_session=db_session, id=id)

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[CalendarEventResponse](
            success=True, data=CalendarEventResponse.from_orm_model(result)
        )

    @override
    async def update(
        self,
        db_session: AsyncSession,
        db_obj: CalendarEvent,
        obj_in: CalendarEventUpdateSchema,
    ) -> DAOResponse[CalendarEventResponse]:
        entity_data = obj_in.model_dump(
            exclude_none=True, exclude=["event_id", "id"]
        ).items()
        result: CalendarEvent = await super().update(
            db_session=db_session, db_obj=db_obj, obj_in=entity_data
        )

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})
        
        return DAOResponse[CalendarEventResponse](
            success=True, data=CalendarEventResponse.from_orm_model(result)
        )
