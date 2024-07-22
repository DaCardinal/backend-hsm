from typing import Any, Dict, TypeVar, Generic, Optional
from pydantic import BaseModel, ConfigDict, ValidationError, model_serializer

T = TypeVar("T")


class DAOResponse(BaseModel, Generic[T]):
    success: bool = False
    error: Optional[str] = None
    data: Optional[T | Any] = None
    meta: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    def __init__(
        self,
        *,
        success: bool,
        data: Optional[T] = None,
        error: Optional[str] = None,
        validation_error: Optional[ValidationError] = None,
        meta: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(success=success, data=data, error=error, **kwargs)
        self.error = "" if error is None else error
        self.meta = meta

        if validation_error:
            self.set_validation_errors(validation_error)

    def set_validation_errors(self, validation_error: ValidationError):
        error_messages = []
        for error in validation_error.errors():
            field = error["loc"][0]
            message = error["msg"]
            error_messages.append(f"{field} validation is incorrect: {message}")
        self.error = "; ".join(error_messages)

    def set_meta(self, meta):
        self.meta = meta

    @model_serializer(when_used="json")
    def dump_model(self) -> Dict[str, Any]:
        result = super().model_dump()

        if not self.meta:
            result.pop("meta", None)
        elif self.meta["total"] == 0:
            result.pop("meta", None)

        return result
