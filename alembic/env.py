import asyncio
from sqlalchemy import pool
from alembic import context
from logging.config import fileConfig
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.db.dbDeclarative import Base
# Core Models
from app.models.accounts import Accounts  # noqa: F401
from app.models.company import Company  # noqa: F401

from app.models.country import Country  # noqa: F401
from app.models.city import City  # noqa: F401
from app.models.region import Region  # noqa: F401
from app.models.address import Addresses  # noqa: F401
from app.models.entity_address import EntityAddress  # noqa: F401

from app.models.media import Media  # noqa: F401
from app.models.entity_media import EntityMedia  # noqa: F401

from app.models.message import Message  # noqa: F401
from app.models.reminder_frequency import ReminderFrequency  # noqa: F401
from app.models.message_recipient import MessageRecipient  # noqa: F401

from app.models.user import User  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.permissions import Permissions  # noqa: F401
from app.models.user_company import UsersCompany  # noqa: F401
from app.models.user_interactions import UserInteractions  # noqa: F401
from app.models.role_permissions import RolePermissions  # noqa: F401
from app.models.user_role import UserRoles  # noqa: F401
from app.models.user_account import UserAccounts  # noqa: F401

from app.models.transaction_type import TransactionType  # noqa: F401
from app.models.payment_type import PaymentTypes  # noqa: F401
from app.models.contract_type import ContractType  # noqa: F401
from app.models.contract import Contract, ContractStatusEnum  # noqa: F401
from app.models.document import Documents  # noqa: F401
from app.models.under_contract import UnderContract  # noqa: F401
from app.models.invoice import Invoice, PaymentStatusEnum  # noqa: F401
from app.models.invoice_item import InvoiceItem  # noqa: F401
from app.models.contract_invoice import ContractInvoice  # noqa: F401
from app.models.contract_documents import ContractDocuments  # noqa: F401

from app.models.transaction import Transaction  # noqa: F401

from app.models.billable import BillableAssoc  # noqa: F401
from app.models.utility import Utilities  # noqa: F401
from app.models.entity_amenities import EntityAmenities  # noqa: F401
from app.models.ammenity import Amenities  # noqa: F401
from app.models.entity_billable import EntityBillable  # noqa: F401

from app.models.property_unit_assoc import PropertyUnitAssoc  # noqa: F401
from app.models.unit import Units  # noqa: F401
from app.models.property import Property  # noqa: F401
from app.models.property_type import PropertyType  # noqa: F401
from app.models.unit_type import UnitType  # noqa: F401
from app.models.property_assignment import PropertyAssignment  # noqa: F401

from app.models.calendar_event import CalendarEvent  # noqa: F401
from app.models.maintenance_request import MaintenanceRequest, MaintenanceStatusEnum  # noqa: F401

from app.models.tour_bookings import Tour  # noqa: F401
from app.models.user_favorites import FavoriteProperties  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
