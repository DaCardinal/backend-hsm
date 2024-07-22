from uuid import UUID
from typing import Annotated
from pydantic import BaseModel, ConfigDict, constr


class Account(BaseModel):
    """
    Model for representing an account.

    Attributes:
        account_id (UUID): The unique identifier for the account.
        bank_account_name (str): The name on the bank account.
        bank_account_number (str): The number of the bank account.
        account_branch_name (str): The branch name of the bank account.
    """

    account_id: UUID
    bank_account_name: Annotated[str, constr(max_length=128)]
    bank_account_number: Annotated[str, constr(max_length=50)]
    account_branch_name: Annotated[str, constr(max_length=128)]

    model_config = ConfigDict(from_attributes=True)
