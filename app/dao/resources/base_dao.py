import asyncio
import inspect
from uuid import UUID
from functools import partial
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Generic,
    Union,
)

from app.db.dbCrud import DBOperations
from app.utils.response import DAOResponse

# schemas
from app.schema.invoice import InvoiceItem
from app.schema.media import MediaBase, Media
from app.schema.billable import Billable, BillableBase
from app.schema.amenity import Amenities, AmenitiesBase
from app.schema.mixins.address_mixin import Address, AddressBase
from app.schema.mixins.contract_mixin import UnderContractSchema
from app.schema.mixins.user_mixins import (
    UserAuthInfo,
    UserEmployerInfo,
    UserEmergencyInfo,
    PastRentalHistory,
    PastRentalHistoryBase,
)

DBModelType = TypeVar("DBModelType")


class BaseDAO(DBOperations, Generic[DBModelType]):
    # nesting type
    NESTED_CHILD = "nested_child"
    NO_NESTED_CHILD = "parents_only"
    IMMEDIATE_CHILD = "immediate_child"

    def __init__(
        self,
        model: Type[DBModelType],
        excludes=[],
        nesting_degree: str = NO_NESTED_CHILD,
    ):
        self.model = model
        self.nesting_degree = nesting_degree

        if self.nesting_degree == self.IMMEDIATE_CHILD:
            self.load_parent_relationships = True
            self.load_child_relationships = False
        elif self.nesting_degree == self.NESTED_CHILD:
            self.load_parent_relationships = True
            self.load_child_relationships = True
        elif self.nesting_degree == self.NO_NESTED_CHILD:
            self.load_parent_relationships = False
            self.load_child_relationships = False

        self.excludes = excludes

    def filter_kwargs_for_method(self, method, kwargs):
        """
        Filters kwargs to only include arguments that are accepted by the method.

        :param method: The method to be called.
        :param kwargs: The keyword arguments to be filtered.
        :return: A dictionary of filtered kwargs.
        """
        method_signature = inspect.signature(method)
        method_params = method_signature.parameters

        return {k: v for k, v in kwargs.items() if k in method_params}

    def get_schema_info(
        self,
        entity_key: str,
        entity_model: Union[str | BaseModel],
        entity_assoc_id: Any,
    ):
        """
        Retrieves the schema information for a specific entity key.

        Args:
            entity_key (str): The key representing the entity detail.
            entity_model (str): The name of the entity model.
            entity_assoc_id (Any): The associated ID of the entity.

        Returns:
            Tuple[Type[BaseModel], Type[BaseModel], str, Any, str]: A tuple containing the base schema class, full schema class, entity model name, associated ID, and foreign key name.
        """
        schema_info = {
            "media": (MediaBase, Media, entity_model, entity_assoc_id, "media_id"),
            "amenities": (
                AmenitiesBase,
                Amenities,
                entity_model,
                entity_assoc_id,
                "amenity_id",
            ),
            "address": (AddressBase, Address, entity_model, None, "address_id"),
            "utilities": (
                BillableBase,
                Billable,
                entity_model,
                entity_assoc_id,
                "billable_id",
            ),
            "user_auth_info": (UserAuthInfo, None, None, None, None),
            "user_employer_info": (UserEmployerInfo, None, None, None, None),
            "user_emergency_info": (UserEmergencyInfo, None, None, None, None),
            "rental_history": (
                PastRentalHistoryBase,
                PastRentalHistory,
                None,
                None,
                "rental_history_id",
            ),
            "contract_info": (UnderContractSchema, None, None, None, None),
            "invoice_items": (InvoiceItem, None, None, None, None),
        }

        return schema_info.get(entity_key, (None, None, None, None, None))

    def determine_schema(self, entity_data, key, full_schema, base_schema, id_key="id"):
        """
        Determines the appropriate schema class based on the provided entity data.

        Args:
            entity_data (dict): The data dictionary to check for the schema key.
            key (str): The key to look for in the entity_data dictionary.
            full_schema (Type[BaseModel]): The full schema class to return if the conditions are met.
            base_schema (Type[BaseModel]): The base schema class to return if the conditions are not met.
            id_key (str, optional): The key to check for existence in the entity data's key. Defaults to "id".

        Returns:
            Type[BaseModel]: The appropriate schema class.
        """
        detail_data = entity_data.get(key)
        if detail_data:
            if isinstance(detail_data, list):
                if detail_data and id_key in detail_data[0]:
                    return full_schema
            elif id_key in detail_data:
                return full_schema
        return base_schema

    def create_detail_method(
        self,
        entity_data: Dict[str, Any],
        entity_key: str,
        method_or_dao: Union[Callable, Any],
        base_schema_class: Type[BaseModel],
        schema_class: Type[BaseModel] = None,
        entity_model: Union[str | BaseModel] = None,
        entity_assoc_id: Any = None,
        foreign_key_name: str = None,
    ) -> Dict[str, Tuple[Callable, Type[BaseModel]]]:
        """
        Creates a dictionary mapping for a specific entity detail method.

        Args:
            entity_data (Dict[str, Any]): The data dictionary for the entity.
            entity_key (str): The key in the entity_data dictionary representing the detail.
            method_or_dao (Union[Callable, Any]): The method or DAO to be used for processing the detail.
            base_schema_class (Type[BaseModel]): The base schema class for the detail.
            schema_class (Type[BaseModel], optional): The full schema class, if different from base_schema_class.
            entity_model (str, optional): The name of the entity model.
            entity_assoc_id (Any, optional): The associated ID of the entity, if applicable.
            foreign_key_name (str, optional): The name of the foreign key, if applicable.

        Returns:
            Dict[str, Tuple[Callable, Type[BaseModel]]]: A dictionary with the entity key mapped to the corresponding method and schema.
        """
        schema = self.determine_schema(
            entity_data, entity_key, schema_class, base_schema_class, foreign_key_name
        )

        if entity_assoc_id and callable(method_or_dao):
            partial_method = partial(
                method_or_dao,
                entity_model=entity_model,
                entity_assoc_id=entity_assoc_id,
            )
        elif entity_model:
            partial_method = partial(method_or_dao, entity_model=entity_model)
        else:
            partial_method = method_or_dao

        return {entity_key: (partial_method, schema)}

    def build_details_methods(
        self,
        entity_data: Dict[str, Any],
        detail_mappings: Dict[str, Callable],
        entity_model: Union[str | BaseModel] = None,
        entity_assoc_id: Any = None,
    ) -> Dict[str, Any]:
        """
        Builds a dictionary of detail methods based on the provided mappings.

        Args:
            entity_data (Dict[str, Any]): The data dictionary for the entity.
            detail_mappings (Dict[str, Callable]): A dictionary mapping entity keys to their corresponding detail methods.
            entity_model (str, optional): The name of the entity model.
            entity_assoc_id (Any, optional): The associated ID of the entity, if applicable.

        Returns:
            Dict[str, Any]: A dictionary with the entity keys mapped to their corresponding detail methods.
        """
        details_methods = {}

        for entity_key, method_or_dao in detail_mappings.items():
            schema_info = self.get_schema_info(
                entity_key, entity_model, entity_assoc_id
            )
            method_dict = self.create_detail_method(
                entity_data, entity_key, method_or_dao, *schema_info
            )

            details_methods.update(method_dict)

        return details_methods

    async def process_entity_details(
        self,
        db_session: AsyncSession,
        entity_id: UUID,
        entity_data: BaseModel,
        details_methods: dict,
        *args,
        **kwargs,
    ):
        """
        Processes entity details by executing the corresponding detail methods.

        Args:
            db_session (AsyncSession): The database session for executing queries.
            entity_id (UUID): The ID of the entity.
            entity_data (BaseModel): The data model for the entity.
            details_methods (dict): A dictionary mapping entity keys to their corresponding detail methods.

        Returns:
            dict: A dictionary containing the results of the detail processing.
        """
        results = {}

        for detail_key, (method, schema) in details_methods.items():
            detail_data = self.extract_model_data(
                entity_data, schema, nested_key=detail_key
            )
            if detail_data:
                filtered_kwargs = self.filter_kwargs_for_method(method, kwargs)
                if isinstance(detail_data, list):
                    results[detail_key] = [
                        await method(
                            db_session,
                            entity_id,
                            schema(**item),
                            *args,
                            **filtered_kwargs,
                        )
                        for item in detail_data
                    ]
                else:
                    results[detail_key] = await method(
                        db_session,
                        entity_id,
                        schema(**detail_data),
                        *args,
                        **filtered_kwargs,
                    )

        # validate errors
        self.validate_errors(results)

        return results

    def validate_errors(self, results):
        """
        Validates the results of the entity detail processing.

        Args:
            results (dict): A dictionary containing the results of the detail processing.

        Raises:
            Exception: If any of the detail processing results contain an error.
        """
        for result_value in results.values():
            items = result_value if isinstance(result_value, list) else [result_value]

            for item in items:
                if isinstance(item, DAOResponse) and not item.success:
                    print("ERROR", item)
                    raise Exception(str(item.error))

    async def handle_entity_details(
        self,
        db_session: AsyncSession,
        entity_data: Dict[str, Any],
        detail_mappings: Dict[str, Callable],
        entity_model: str = None,
        entity_assoc_id: Any = None,
        *args,
        **kwargs,
    ):
        """
        Handles the processing of entity details by building and processing the detail methods.

        Args:
            db_session (AsyncSession): The database session for executing queries.
            entity_data (Dict[str, Any]): The data dictionary for the entity.
            detail_mappings (Dict[str, Callable]): A dictionary mapping entity keys to their corresponding detail methods.
            entity_model (str, optional): The name of the entity model.
            entity_assoc_id (Any, optional): The associated ID of the entity, if applicable.
        """
        details_methods = self.build_details_methods(
            entity_data, detail_mappings, entity_model, entity_assoc_id
        )

        if set(details_methods.keys()) & set(entity_data.keys()):
            await self.process_entity_details(
                db_session,
                entity_assoc_id,
                entity_data,
                details_methods,
                *args,
                **kwargs,
            )

    def decompose_dict(self, d):
        """
        Decomposes a nested dictionary or list into a flattened dictionary.
        """
        if isinstance(d, dict):
            return {
                key: (
                    self.decompose_dict(value.to_dict())
                    if hasattr(value, "to_dict")
                    else self.decompose_dict(value)
                )
                for key, value in d.items()
            }
        if isinstance(d, list):
            return [self.decompose_dict(item) for item in d]
        return d

    def exclude_keys(self, original_dict: Dict, keys_to_exclude: List[str]):
        return {k: v for k, v in original_dict.items() if k not in keys_to_exclude}

    async def validate_ids(
        self,
        db_session: AsyncSession,
        validations: List[Tuple[DBOperations, Dict]],
    ) -> Union[None, DAOResponse]:
        queries = [
            dao.query(db_session, filters=filters, single=True)
            for dao, filters in validations
        ]
        results = await asyncio.gather(*queries)

        for result, (dao, filters) in zip(results, validations):
            if not result:
                key = list(filters.keys())[0]
                return DAOResponse(
                    success=False,
                    error=f"{dao.model.__name__}: {key} does not exist",
                    data={},
                )

        return None

    # async def _validate_ids(
    #     self,
    #     db_session: AsyncSession,
    #     client_id: UUID,
    #     employee_id: UUID,
    #     contract_id: str,
    #     property_unit_assoc: UUID,
    # ) -> Union[None, DAOResponse]:
    #     validations = [
    #         (self.user_dao, {"user_id": client_id}),
    #         (self.user_dao, {"user_id": employee_id}),
    #         (self.contract_dao, {"contract_number": contract_id}),
    #         (self.property_unit_assoc_dao, {"property_unit_assoc_id": property_unit_assoc}),
    #     ]

    #     return await self.validate_ids(db_session, validations)

    def extract_model_data(
        self, data: dict, schema: Type[BaseModel], nested_key: Optional[str] = None
    ) -> Union[List[dict] | dict]:
        """
        Extracts model data from a dictionary based on the provided schema.

        Args:
            data (dict): The dictionary containing the data to be extracted.
            schema (Type[BaseModel]): The schema class to use for extracting the data.
            nested_key (Optional[str], optional): The key in the dictionary representing nested data.

        Returns:
            Union[List[dict], dict]: The extracted data.
        """
        data = data.get(nested_key, {}) if nested_key else data

        if not data:
            return None

        if isinstance(data, list):
            return [
                {key: item[key] for key in item if key in schema.model_fields}
                for item in data
            ]

        return {key: data[key] for key in data if key in schema.model_fields}
