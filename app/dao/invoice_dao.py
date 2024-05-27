from functools import partial
from typing import Dict, Type
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base_dao import BaseDAO
from app.models import Invoice
from app.utils import DAOResponse
from app.models import InvoiceItem
from app.schema import InvoiceCreateSchema, ContractResponse, InvoiceItemBase, InvoiceResponse

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
        
    async def add_invoice_details(self, db_session: AsyncSession, invoice_number: str,  invoice_info: InvoiceItemBase, invoice : Invoice= None):
        invoice_item_dao = BaseDAO(InvoiceItem)

        try:
            if not isinstance(invoice_info, list):
                invoice_info = [invoice_info]

            for invoice_item in invoice_info:
                invoice_item : InvoiceItemBase = invoice_item

                invoice_item_obj = {
                    "description": invoice_item.description,
                    "invoice_number": invoice.invoice_number,
                    "quantity": invoice_item.quantity,
                    "unit_price": invoice_item.unit_price,
                    "total_price": invoice_item.total_price,
                }

                # Check if the contract info already exists
                if "invoice_number" in invoice_item.model_fields:
                    existing_invoice_item : InvoiceItem = await invoice_item_dao.query(db_session=db_session, filters=invoice_item_obj, single=True)
                else: 
                    existing_invoice_item = None
                
                if existing_invoice_item:
                    invoice_item_details = await invoice_item_dao.update(db_session=db_session, db_obj=existing_invoice_item, obj_in=invoice_item_obj.items())
                else:
                    invoice_item_details = await invoice_item_dao.create(db_session=db_session, obj_in=invoice_item_obj)

                # commit object to db session
                await invoice_item_dao.commit_and_refresh(db_session, invoice_item_details)

            return invoice_item_details
        except ValidationError as e:
            return DAOResponse(success=False, validation_error=str(e))
        except Exception as e:
            return DAOResponse(success=False, error=f"Fatal {str(e)}")