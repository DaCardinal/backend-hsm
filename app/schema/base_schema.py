from typing import List, Optional, Type, Dict
from pydantic import BaseModel, create_model
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import inspect

SchemasDictType = Dict[str, Type[BaseModel]]

def generate_schemas_for_sqlalchemy_model(model: Type[DeclarativeMeta], excludes : List[str] = ['id']) -> Dict[str, Type[BaseModel]]:
    """
    Generates Pydantic schemas for a given SQLAlchemy model.
    Returns a dictionary with 'model_schema', 'create_schema', and 'update_schema'.
    """
    columns = {c.name: (c.type.python_type, ...) for c in inspect(model).c}
    primary_keys = [key.name for key in inspect(model).primary_key]

    model_schema = create_model(
        f"{model.__name__}ModelSchema",
        **{name: (typ, None) for name, (typ, _) in columns.items()},
        __base__=BaseModel
    )

    default_excludes : List[str] = ['created_at', 'updated_at']
    default_excludes.extend(excludes)
    
    create_schema_fields = {name: (typ, ...) for name, (typ, _) in columns.items() if name not in default_excludes}
    create_schema = create_model(
        f"{model.__name__}CreateSchema",
        **create_schema_fields,
        __base__=BaseModel
    )

    update_schema = create_model(
        f"{model.__name__}UpdateSchema",
        **{name: (Optional[typ], None) for name, (typ, _) in columns.items()},
        __base__=BaseModel
    )
    
    return {
        "model_schema": model_schema,
        "create_schema": create_schema,
        "update_schema": update_schema,
        "primary_keys": primary_keys
    }
