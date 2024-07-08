from uuid import UUID
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.contract_dao import ContractDAO
from app.router.base_router import BaseCRUDRouter
from app.schema import ContractSchema, ContractCreateSchema, ContractUpdateSchema, UnderContractCreate

class ContractRouter(BaseCRUDRouter):

    def __init__(self, prefix: str = "", tags: List[str] = []):

        # initialize router dao
        ContractSchema["create_schema"] = ContractCreateSchema
        ContractSchema["update_schema"] = ContractUpdateSchema
        self.dao : ContractDAO = ContractDAO(nesting_degree=BaseCRUDRouter.NO_NESTED_CHILD, excludes=[''])
        
        super().__init__(dao=self.dao, schemas=ContractSchema, prefix=prefix,tags = tags)
        self.register_routes()

    def register_routes(self):    
        @self.router.post("/add_user_lease")
        async def add_user_lease(user_id: UUID, contract_id: str, db: AsyncSession = Depends(self.get_db)):
            user = ''
            pass
            
            if user is None:
                raise HTTPException(status_code=404, detail="Error adding lease.")
            
            return user