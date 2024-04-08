from typing import TypeVar, Generic, Optional
from pydantic import BaseModel, ValidationError, validator

T = TypeVar("T")

class DAOResponse(BaseModel, Generic[T]):
    success: bool = False
    error: Optional[str] = None
    data: Optional[T] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True
    
    def __init__(self, *, success: bool, data: Optional[T] = None, error: Optional[str] = None, validation_error: Optional[ValidationError] = None, **kwargs):
        super().__init__(success=success, data=data, error=error, **kwargs)
        self.error = "" if error is None else error

        if validation_error:
            self.set_validation_errors(validation_error)

    def set_validation_errors(self, validation_error: ValidationError):
        error_messages = []
        for error in validation_error.errors():
            field = error['loc'][0]
            message = error['msg']
            error_messages.append(f"{field} validation is incorrect: {message}")
        self.error = "; ".join(error_messages)
    