from uuid import UUID
from typing import Any, List, Union
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

# daos
from app.dao.base_dao import BaseDAO

# utils
from app.utils.response import DAOResponse

# models
from app.models.transaction import Transaction

# schemas
from app.schema.enums import PaymentStatus
from app.schema.transaction import TransactionResponse, TransactionCreateSchema


class TransactionDAO(BaseDAO[Transaction]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = Transaction
        self.primary_key = "transaction_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: TransactionCreateSchema
    ) -> DAOResponse[TransactionResponse]:
        try:
            # extract base information
            transaction_info = self.extract_model_data(
                TransactionCreateSchema(**obj_in).model_dump(exclude=[""]),
                TransactionCreateSchema,
            )
            new_transaction: Transaction = await super().create(
                db_session=db_session, obj_in=transaction_info
            )

            # commit object to db session
            await self.commit_and_refresh(db_session, new_transaction)

            return DAOResponse[TransactionResponse](
                success=True, data=TransactionResponse.from_orm_model(new_transaction)
            )
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[TransactionResponse](
                success=False, error=f"Fatal {str(e)}"
            )

    @override
    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> DAOResponse[List[TransactionResponse]]:
        result = await super().get_all(
            db_session=db_session, offset=offset, limit=limit
        )

        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[TransactionResponse]](
            success=True, data=[TransactionResponse.from_orm_model(r) for r in result]
        )

    @override
    async def get(
        self, db_session: AsyncSession, id: Union[UUID | Any | int]
    ) -> DAOResponse[TransactionResponse]:
        result: Transaction = await super().get(db_session=db_session, id=id)

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[TransactionResponse](
            success=True, data=TransactionResponse.from_orm_model(result)
        )

    async def get_transaction_status(self, db_session: AsyncSession):
        try:
            return DAOResponse(
                success=True,
                data={status.name: status.value for status in PaymentStatus},
            )
        except Exception as e:
            return DAOResponse[str](success=False, error=f"Fatal {str(e)}")
