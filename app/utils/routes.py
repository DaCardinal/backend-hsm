from fastapi import APIRouter, FastAPI
from app.router import *

router = APIRouter()

def configure_routes(app: FastAPI):
    app.include_router(router)
    
    # Create an instance of AuthRouter
    app.include_router(AuthRouter(prefix="/auth", tags=["Auth"]).router)
    
    # Create an instance of UserRouter
    app.include_router(UserRouter(prefix="/users", tags=["Users"]).router)
    
    # Create an instance of RoleRouter
    app.include_router(RoleRouter(prefix="/roles", tags=["Roles"]).router)
    
    # Create an instance of PermissionRouter
    app.include_router(PermissionRouter(prefix="/permissions", tags=["Permissions"]).router)
    
    # Create an instance of PropertyRouter
    app.include_router(PropertyRouter(prefix="/property", tags=["Property"]).router)
    
    # Create an instance of PropertyUniRouter
    app.include_router(PropertyUnitRouter(prefix="/units", tags=["Units"]).router)
    
    # Create an instance of AmmenitiesRouter
    app.include_router(AmmenitiesRouter(prefix="/ammenities", tags=["Ammenities"]).router)
    
    # Create an instance of MediaRouter
    app.include_router(MediaRouter(prefix="/media", tags=["Media"]).router)
    
    # Create an instance of MessageRouter
    app.include_router(MessageRouter(prefix="/messages", tags=["Message"]).router)
    
    # Create an instance of ContractRouter
    app.include_router(ContractRouter(prefix="/contract", tags=["Contract"]).router)
    
    # Create an instance of ContractTypeRouter
    app.include_router(ContractTypeRouter(prefix="/contract_type", tags=["ContractType"]).router)
    
    # Create an instance of Transaction_typeRouter
    app.include_router(TransactionTypeRouter(prefix="/transaction_type", tags=["TransactionType"]).router)
    
    # Create an instance of PaymenttypeRouter
    app.include_router(PaymentTypeRouter(prefix="/payment_type", tags=["PaymentType"]).router)
    
    # Create an instance of InvoiceRouter
    app.include_router(InvoiceRouter(prefix="/invoice", tags=["Invoice"]).router)
    
    # Create an instance of TransactionRouter
    app.include_router(TransactionRouter(prefix="/transaction", tags=["Transaction"]).router)
    
    # Create an instance of CompanyRouter
    # app.include_router(CompanyRouter(prefix="/company", tags=["Company"]).router)
