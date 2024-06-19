from uuid import UUID
from functools import partial
from pydantic import ValidationError
from typing_extensions import override
from typing import Any, List, Type, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select
from sqlalchemy.orm import joinedload


from app.dao.base_dao import BaseDAO
from app.dao.invoice_item_dao import InvoiceItemDAO
from app.models import Invoice, UnderContract, User, Contract, ContractInvoice, ContractStatusEnum, PaymentStatusEnum, ContractType
from app.utils import DAOResponse
from app.models import InvoiceItem
from app.schema import InvoiceCreateSchema, InvoiceItemBase, InvoiceResponse

class InvoiceDAO(BaseDAO[Invoice]):
    def __init__(self, model: Type[Invoice], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        super().__init__(model, load_parent_relationships, load_child_relationships, excludes=excludes)
        self.primary_key = "invoice_number"

    @override
    async def create(self, db_session: AsyncSession, obj_in: InvoiceCreateSchema) -> DAOResponse[InvoiceResponse]:
        try:

            # extract base information
            invoice_info = self.extract_model_data(InvoiceCreateSchema(**obj_in).model_dump(exclude=["invoice_items"]), InvoiceCreateSchema)
            new_invoice: Invoice = await super().create(db_session=db_session, obj_in=invoice_info)

            details_methods = {
                'invoice_items': (partial(self.add_invoice_details, invoice=new_invoice), InvoiceItemBase)
            }

            if set(details_methods.keys()).issubset(set(obj_in.keys())):
                await self.process_entity_details(db_session, new_invoice.invoice_number, obj_in, details_methods)

            # commit object to db session
            await self.commit_and_refresh(db_session, new_invoice)
            
            return DAOResponse[InvoiceResponse](success=True, data=InvoiceResponse.from_orm_model(new_invoice))
        except ValidationError as e:
            return DAOResponse(success=False, data=str(e))
        except Exception as e:
            await db_session.rollback()
            return DAOResponse[InvoiceResponse](success=False, error=f"Fatal {str(e)}")
    
    @override
    async def get_all(self, db_session: AsyncSession, offset=0, limit=100) -> DAOResponse[List[InvoiceResponse]]:
        result = await super().get_all(db_session=db_session, offset=offset, limit=limit)
        
        # check if no result
        if not result:
            return DAOResponse(success=True, data=[])

        return DAOResponse[List[InvoiceResponse]](success=True, data=[InvoiceResponse.from_orm_model(r) for r in result])
    
    @override
    async def get(self, db_session: AsyncSession, id: Union[UUID | Any | int]) -> DAOResponse[InvoiceResponse]:
        result : Invoice = await super().get(db_session=db_session, id=id)

        # check if no result
        if not result:
            return DAOResponse(success=True, data={})

        return DAOResponse[InvoiceResponse](success=True, data=InvoiceResponse.from_orm_model(result))
    
    # TODO Remove
    async def get_leases_due_old(self, db_session: AsyncSession, contract_type_name: str = "lease", user_id : str = None, offset=0, limit=100):
        under_contract_dao = BaseDAO(UnderContract)
        contract_dao = BaseDAO(Contract)
        user_dao = BaseDAO(User)
        
        filters = [
            ContractType.contract_type_name == contract_type_name,
            UnderContract.contract_status == ContractStatusEnum.active.name,
            Invoice.status == PaymentStatusEnum.pending.name
        ]
        
        if user_id:
            filters.append(UnderContract.client_id == user_id)

        lease_due_stmt = select(Invoice).join(
            ContractInvoice, ContractInvoice.invoice_number == Invoice.invoice_number
        ).join(
            Contract, Contract.contract_id == ContractInvoice.contract_id
        ).join(
            UnderContract, UnderContract.contract_id == Contract.contract_id
        ).join(
            ContractType, Contract.contract_type_id == ContractType.contract_type_id
        ).filter(
            and_(*filters)
        )

        leases_due_result = await db_session.execute(lease_due_stmt)
        leases_due = leases_due_result.scalars().all()

        return leases_due
    
    async def get_leases_due(self, db_session: AsyncSession, contract_type_name: str = "lease", user_id : str = None, offset=0, limit=100):

        filters = {
            "status": PaymentStatusEnum.pending.name,
            "ContractType.contract_type_name": contract_type_name,
            # "UnderContract.contract_status": ContractStatusEnum.active.name,
        }
        
        join_conditions = [
            (ContractInvoice, ContractInvoice.invoice_number == Invoice.invoice_number),
            (Contract, Contract.contract_id == ContractInvoice.contract_id),
            (UnderContract, UnderContract.contract_id == Contract.contract_id),
            (ContractType, ContractType.contract_type_id == Contract.contract_type_id)
        ]

        if user_id:
            filters["UnderContract.client_id"] = user_id
        
        options = [
            joinedload(Invoice.contracts),
            joinedload(Invoice.transaction),
            joinedload(Invoice.invoice_items)
        ]
        
        return await self.query_on_joins(
            db_session=db_session, 
            filters=filters, 
            join_conditions=join_conditions, 
            options=options,
        )

    async def add_invoice_details(self, db_session: AsyncSession, invoice_number: str,  invoice_info: InvoiceItemBase, invoice : Invoice = None):
        invoice_item_dao = InvoiceItemDAO(InvoiceItem)

        try:
            if not isinstance(invoice_info, list):
                invoice_info = [invoice_info]

            for invoice_item in invoice_info:
                invoice_item : InvoiceItemBase = invoice_item

                invoice_item_obj = {
                    "description": invoice_item.description,
                    "invoice_number": invoice_number,
                    "quantity": invoice_item.quantity,
                    "unit_price": invoice_item.unit_price,
                    "total_price": invoice_item.total_price,
                }

                if "invoice_number" in invoice_item.model_fields:
                    existing_invoice_item : InvoiceItem = await invoice_item_dao.query(db_session=db_session, filters=invoice_item_obj, single=True)
                else: 
                    existing_invoice_item = None
                
                if existing_invoice_item:
                    invoice_item_details : InvoiceItem = await invoice_item_dao.update(db_session=db_session, db_obj=existing_invoice_item, obj_in=invoice_item_obj.items())
                else:
                    invoice_item_details : InvoiceItem = await invoice_item_dao.create(db_session=db_session, obj_in={**invoice_item_obj})
                    
                # commit object to db session
                await invoice_item_dao.commit_and_refresh(db_session, invoice_item_details)

            return invoice_item_details
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            return DAOResponse(success=False, error=f"Fatal {str(e)}")