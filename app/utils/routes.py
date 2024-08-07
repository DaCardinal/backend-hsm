from fastapi import APIRouter, FastAPI

from app.router.auth_router import AuthRouter
from app.router.user_router import UserRouter
from app.router.role_router import RoleRouter
from app.router.permission_router import PermissionRouter
from app.router.property_router import PropertyRouter
from app.router.property_unit_router import PropertyUnitRouter
from app.router.amenities_router import AmenitiesRouter
from app.router.media_router import MediaRouter
from app.router.message_router import MessageRouter
from app.router.under_contract_router import UnderContractRouter
from app.router.property_assignment_router import PropertyAssignmentRouter
from app.router.contract_router import ContractRouter
from app.router.contract_type_router import ContractTypeRouter
from app.router.transaction_type_router import TransactionTypeRouter
from app.router.payment_type_router import PaymentTypeRouter
from app.router.invoice_router import InvoiceRouter
from app.router.transaction_router import TransactionRouter
from app.router.maintenance_request_router import MaintenanceRequestRouter
from app.router.calendar_event_router import CalendarEventRouter
from app.router.tour_bookings_router import TourBookingRouter
from app.router.utilities_router import UtilitiesRouter

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
    app.include_router(
        PermissionRouter(prefix="/permissions", tags=["Permissions"]).router
    )

    # Create an instance of PropertyRouter
    app.include_router(PropertyRouter(prefix="/property", tags=["Property"]).router)

    # Create an instance of PropertyUniRouter
    app.include_router(PropertyUnitRouter(prefix="/units", tags=["Units"]).router)

    # Create an instance of AmmenitiesRouter
    app.include_router(
        AmenitiesRouter(prefix="/ammenities", tags=["Ammenities"]).router
    )

    # Create an instance of MediaRouter
    app.include_router(MediaRouter(prefix="/media", tags=["Media"]).router)

    # Create an instance of MessageRouter
    app.include_router(MessageRouter(prefix="/messages", tags=["Message"]).router)

    # Create an instance of UnderContractRouter
    app.include_router(
        UnderContractRouter(
            prefix="/assign_contracts", tags=["ContractAssignments"]
        ).router
    )

    # Create an instance of PropertyAssignmentRouter
    app.include_router(
        PropertyAssignmentRouter(
            prefix="/property_assignment", tags=["PropertyAssignment"]
        ).router
    )

    # Create an instance of ContractRouter
    app.include_router(ContractRouter(prefix="/contract", tags=["Contract"]).router)

    # Create an instance of ContractTypeRouter
    app.include_router(
        ContractTypeRouter(prefix="/contract_type", tags=["ContractType"]).router
    )

    # Create an instance of Transaction_typeRouter
    app.include_router(
        TransactionTypeRouter(
            prefix="/transaction_type", tags=["TransactionType"]
        ).router
    )

    # Create an instance of PaymenttypeRouter
    app.include_router(
        PaymentTypeRouter(prefix="/payment_type", tags=["PaymentType"]).router
    )

    # Create an instance of InvoiceRouter
    app.include_router(InvoiceRouter(prefix="/invoice", tags=["Invoice"]).router)

    # Create an instance of TransactionRouter
    app.include_router(
        TransactionRouter(prefix="/transaction", tags=["Transaction"]).router
    )

    # Create an instance of CompanyRouter
    # app.include_router(CompanyRouter(prefix="/company", tags=["Company"]).router)

    # Create an instance of MaintenanceRequestRouter
    app.include_router(
        MaintenanceRequestRouter(
            prefix="/maintenance_request", tags=["MaintenanceRequest"]
        ).router
    )

    # Create an instance of CalendarEventRouter
    app.include_router(
        CalendarEventRouter(prefix="/calendar_event", tags=["CalendarEvent"]).router
    )

    # Create an instance of TourBookingRouter
    app.include_router(
        TourBookingRouter(prefix="/tour_booking", tags=["PropertyTours"]).router
    )

    # Create an instance of UtilitiesRouter
    app.include_router(UtilitiesRouter(prefix="/utilities", tags=["Utilities"]).router)
