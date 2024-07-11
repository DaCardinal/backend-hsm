from uuid import UUID
from functools import partial
import uuid
from typing import Any, List, Union
from pydantic import ValidationError
from sqlalchemy.orm import joinedload
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

# utils
from app.utils import DAOResponse

# daos
from app.dao.base_dao import BaseDAO
from app.dao.invoice_item_dao import InvoiceItemDAO

# schemas
from app.schema.invoice import InvoiceCreateSchema, InvoiceItemBase, InvoiceDueResponse, InvoiceResponse

# models
from app.models import Invoice, InvoiceItem, UnderContract, Contract, ContractInvoice, ContractStatusEnum, PaymentStatusEnum, ContractType

class InvoiceDAO(BaseDAO[Invoice]):
    def __init__(self, excludes = [], nesting_degree : str = BaseDAO.NO_NESTED_CHILD):
        self.model = Invoice
        self.primary_key = "invoice_number"
        self.invoice_item_dao = InvoiceItemDAO(InvoiceItem)

        super().__init__(self.model, nesting_degree = nesting_degree, excludes=excludes)

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
    
    async def get_leases_due(self, db_session: AsyncSession, contract_type_name: str = "lease", user_id : str = None, offset=0, limit=100):

        filters = {
            "status": PaymentStatusEnum.pending.name,
            "ContractType.contract_type_name": contract_type_name,
            "Contract.contract_status": str(ContractStatusEnum.active.name),
            "UnderContract.contract_status": str(ContractStatusEnum.active.name),
        }
        
        join_conditions = [
            (ContractInvoice, ContractInvoice.invoice_number == Invoice.invoice_number),
            (Contract, Contract.contract_id == ContractInvoice.contract_id),
            (UnderContract, UnderContract.contract_id == Contract.contract_id),
            (ContractType, ContractType.contract_type_id == Contract.contract_type_id)
        ]

        if user_id:
            filters["UnderContract.client_id"] = uuid.UUID(user_id)
        
        options = [
            joinedload(Invoice.contracts),
            joinedload(Invoice.transaction),
            joinedload(Invoice.invoice_items)
        ]
        query_result = await self.query_on_joins(
            db_session=db_session, 
            filters=filters, 
            join_conditions=join_conditions, 
            options=options,
        )
        
        return DAOResponse[List[InvoiceDueResponse]](success=True, data=[InvoiceDueResponse.from_orm_model(r) for r in query_result])

    async def add_invoice_details(self, db_session: AsyncSession, invoice_number: str,  invoice_info: InvoiceItemBase, invoice : Invoice = None):

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

                # Update if reference id found
                if invoice_item.reference_id:
                    invoice_item_obj["reference_id"] = invoice_item.reference_id

                if "invoice_number" in invoice_item.model_fields:
                    existing_invoice_item : InvoiceItem = await self.invoice_item_dao.query(db_session=db_session, filters=invoice_item_obj, single=True)
                else: 
                    existing_invoice_item = None
                
                if existing_invoice_item:
                    invoice_item_details : InvoiceItem = await self.invoice_item_dao.update(db_session=db_session, db_obj=existing_invoice_item, obj_in=invoice_item_obj.items())
                else:
                    invoice_item_details : InvoiceItem = await self.invoice_item_dao.create(db_session=db_session, obj_in={**invoice_item_obj})
                    
                # commit object to db session
                await self.invoice_item_dao.commit_and_refresh(db_session, invoice_item_details)

            return invoice_item_details
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            return DAOResponse(success=False, error=f"Fatal {str(e)}")