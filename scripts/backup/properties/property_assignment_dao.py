from uuid import UUID
from typing import Any, List, Union
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.resources.base_dao import BaseDAO
from app.models.property_assignment import PropertyAssignment

# schemas
from app.schema.property import PropertyAssignmentResponse
from app.schema.property_assignment import PropertyAssignmentCreate

# utils
from app.utils.response import DAOResponse


class PropertyAssignmentDAO(BaseDAO[PropertyAssignment]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = PropertyAssignment
        self.primary_key = "property_assignment_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: Union[PropertyAssignmentCreate]
    ) -> DAOResponse:
        try:
            property_assignment: PropertyAssignment = await super().create(
                db_session=db_session, obj_in=obj_in
            )

            return DAOResponse[PropertyAssignmentResponse](
                success=True,
                data=PropertyAssignmentResponse.from_orm_model(property_assignment),
            )
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Fatal {str(e)}")

    @override
    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> DAOResponse[List[PropertyAssignmentResponse]]:
        result = await super().get_all(
            db_session=db_session, offset=offset, limit=limit
        )

        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[PropertyAssignmentResponse]](
            success=True,
            data=[PropertyAssignmentResponse.from_orm_model(r) for r in result],
        )

    @override
    async def get(
        self, db_session: AsyncSession, id: Union[UUID | Any | int]
    ) -> DAOResponse[PropertyAssignmentResponse]:
        result: PropertyAssignment = await super().get(db_session=db_session, id=id)

        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[PropertyAssignmentResponse](
            success=True, data=PropertyAssignmentResponse.from_orm_model(result)
        )
