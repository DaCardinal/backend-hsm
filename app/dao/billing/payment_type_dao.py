from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# dao
from app.dao.resources.base_dao import BaseDAO

# model
from app.models.payment_type import PaymentTypes


class PaymentTypeDAO(BaseDAO[PaymentTypes]):
    def __init__(self, excludes=[], nesting_degree: str = BaseDAO.NO_NESTED_CHILD):
        self.model = PaymentTypes
        self.primary_key = "payment_type_id"

        super().__init__(self.model, nesting_degree=nesting_degree, excludes=excludes)

    async def get_existing_payment_type(
        self, db_session: AsyncSession, payment_type: str
    ) -> Optional[PaymentTypes]:
        payment_type_result = await self.query(
            db_session=db_session,
            filters={"payment_type_name": payment_type},
            single=True,
        )

        if not payment_type_result:
            raise NoResultFound("Payment type does not exist")

        return payment_type_result
