from uuid import UUID
from typing import Any, List, Union
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import DAOResponse
from app.dao.base_dao import BaseDAO
from app.models import MaintenanceRequest
from app.schema import MaintenanceRequestCreateSchema, MaintenanceRequestResponse, MaintenanceRequestBase, MaintenanceRequestUpdateSchema

class MaintenanceRequestDAO(BaseDAO[MaintenanceRequest]):
    def __init__(self, excludes = [], nesting_degree : str = BaseDAO.NO_NESTED_CHILD):
        self.model = MaintenanceRequest
        self.primary_key = "task_number"

        super().__init__(self.model, nesting_degree = nesting_degree, excludes=excludes)

    @override
    async def create(self, db_session: AsyncSession, obj_in: MaintenanceRequestCreateSchema) -> DAOResponse[MaintenanceRequestResponse]:
        try:

            # extract base information
            maintenance_request_info = self.extract_model_data(obj_in, MaintenanceRequestBase)
            new_maintenance_request: MaintenanceRequest = await super().create(db_session=db_session, obj_in={**maintenance_request_info})
            
            # commit object to db session
            await self.commit_and_refresh(db_session, new_maintenance_request)
            
            return DAOResponse[MaintenanceRequestResponse](success=True, data=MaintenanceRequestResponse.from_orm_model(new_maintenance_request))
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[MaintenanceRequestResponse](success=False, error=f"Fatal {str(e)}")
    
    @override
    async def get_all(self, db_session: AsyncSession, offset=0, limit=100) -> DAOResponse[List[MaintenanceRequestResponse]]:
        result = await super().get_all(db_session=db_session, offset=offset, limit=limit)
        
        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[MaintenanceRequestResponse]](success=True, data=[MaintenanceRequestResponse.from_orm_model(r) for r in result])
    
    @override
    async def get(self, db_session: AsyncSession, id: Union[UUID | Any | int]) -> DAOResponse[MaintenanceRequestResponse]:
        result : MaintenanceRequest = await super().get(db_session=db_session, id=id)

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[MaintenanceRequestResponse](success=True, data=MaintenanceRequestResponse.from_orm_model(result))
    
    @override
    async def  update(self, db_session: AsyncSession, db_obj: MaintenanceRequest, obj_in: MaintenanceRequestUpdateSchema) -> DAOResponse[MaintenanceRequestResponse]:
        entity_data = obj_in.model_dump(exclude_none=True, exclude=["task_number", "id"]).items()
        
        result : MaintenanceRequest = await super().update(db_session=db_session, db_obj=db_obj, obj_in=entity_data)

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})
        
        return DAOResponse[MaintenanceRequestResponse](success=True, data=MaintenanceRequestResponse.from_orm_model(result))
