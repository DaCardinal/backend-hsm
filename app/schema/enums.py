from enum import Enum


class GenderEnum(str, Enum):
    """
    Enumeration for gender types.

    Attributes:
        male (str): Represents male gender.
        female (str): Represents female gender.
        other (str): Represents other genders.
    """

    male = "male"
    female = "female"
    other = "other"


class AddressTypeEnum(str, Enum):
    """
    Enumeration for address types.

    Attributes:
        billing (str): Represents a billing address.
        mailing (str): Represents a mailing address.
    """

    billing = "billing"
    mailing = "mailing"


class PropertyStatus(str, Enum):
    """
    Enumeration for property status types.

    Attributes:
        available (str): Represents an available property status.
        unavailable (str): Represents an unavailable property status.
    """

    available = "available"
    unavailable = "unavailable"


class PropertyType(str, Enum):
    """
    Enumeration for property types.

    Attributes:
        residential (str): Represents a residential property.
        commercial (str): Represents a commercial property.
        industrial (str): Represents an industrial property.
    """

    residential = "residential"
    commercial = "commercial"
    industrial = "industrial"


class ContractStatus(str, Enum):
    """
    Enumeration for contract status types.

    Attributes:
        active (str): Represents an active contract.
        expired (str): Represents an expired contract.
        terminated (str): Represents a terminated contract.
    """

    active = "active"
    inactive = "inactive"
    expired = "expired"
    pending = "pending"
    terminated = "terminated"


class InvoiceType(str, Enum):
    lease = "lease"
    maintenance = "maintenance"
    other = "other"
    general = "general"


class PaymentStatus(str, Enum):
    """
    Enumeration for payment status types.

    Attributes:
        pending (str): Represents a pending payment status.
        completed (str): Represents a completed payment status.
        cancelled (str): Represents a cancelled payment status.
        reversal (str): Represents a reversal payment status.
    """

    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"
    reversal = "reversal"


class MaintenanceStatus(str, Enum):
    """
    Enumeration for maintenance status types.

    Attributes:
        pending (str): Represents a pending maintenance status.
        in_progress (str): Represents an in-progress maintenance status.
        completed (str): Represents a completed maintenance status.
        cancelled (str): Represents a cancelled maintenance status.
    """

    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class EventType(str, Enum):
    """
    Enumeration for event type.

    Attributes:
        inspection (str): Represents an inspection event.
        meeting (str): Represents a meeting event.
        other (str): Represents other types of events.
    """

    inspection = "inspection"
    meeting = "meeting"
    other = "other"
    birthday = "birthday"
    holiday = "holiday"
    maintenance_request = "maintenance_request"


class CalendarStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class TourType(str, Enum):
    """
    Enumeration for tour type.

    Attributes:
        in_person (str): Represents an in-person tour.
        virtual (str): Represents a virtual tour.
    """

    in_person = "in_person"
    virtual = "virtual"


class TourStatus(str, Enum):
    """
    Enumeration for tour status.

    Attributes:
        incoming (str): Represents an incoming tour.
        completed (str): Represents a completed tour.
        cancelled (str): Represents a cancelled tour.
    """

    incoming = "incoming"
    completed = "completed"
    cancelled = "cancelled"
