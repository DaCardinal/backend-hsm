from typing import List, Type, TypeVar, Generic, Dict, Any, Union, Optional
from uuid import UUID
from sqlalchemy import and_, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect
from sqlalchemy.orm import selectinload

from app.utils.response import DAOResponse

DBModelType = TypeVar("DBModelType")


class UtilsMixin:
    def is_valid_uuid(uuid_to_test, version=4):
        try:
            uuid_obj = UUID(uuid_to_test, version=version)
        except ValueError:
            return str(uuid_to_test)

        return uuid_obj

    async def commit_and_refresh(self, db_session: AsyncSession, obj: DBModelType):
        try:
            await db_session.commit()
            await db_session.refresh(obj)
            return obj
        except Exception as e:
            await db_session.rollback()
            return DAOResponse(success=False, error=f"Error committing data: {str(e)}")


class CreateMixin(UtilsMixin):
    model: Type[DBModelType]

    async def create(self, db_session: AsyncSession, obj_in) -> DBModelType:
        db_obj = self.model(**obj_in)
        db_session.add(db_obj)

        return await self.commit_and_refresh(db_session=db_session, obj=db_obj)


class ReadMixin(UtilsMixin):
    model: Type[DBModelType]
    load_parent_relationships: bool

    async def get(
        self, db_session: AsyncSession, id: Union[UUID | Any | int], skip=0, limit=100
    ) -> DBModelType:
        # check if uuid
        gen_primary_id = UtilsMixin.is_valid_uuid(id)

        # define primary key
        # primary_keys = [(key.name, key) for key in inspect(self.model).primary_key]
        # primary_key = primary_keys[0]
        primary_key = self.primary_key

        mapper = inspect(self.model)
        relationships = [relationship.key for relationship in mapper.relationships]
        query_options = (
            [selectinload(getattr(self.model, attr)) for attr in relationships]
            if self.load_parent_relationships
            else []
        )

        # find model object based on primary key
        filter = {f"{primary_key}": gen_primary_id}
        conditions = [getattr(self.model, k) == v for k, v in filter.items()]
        query = (
            select(self.model)
            .filter(and_(*conditions))
            .options(*query_options)
            .offset(skip)
            .limit(limit)
        )

        executed_query = await db_session.execute(query)
        result = executed_query.scalar_one_or_none()

        return result

    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> list[DBModelType]:
        # dynamically access the relationship attribute using getattr
        mapper = inspect(self.model)
        relationships = [relationship.key for relationship in mapper.relationships]
        query_options = (
            [selectinload(getattr(self.model, attr)) for attr in relationships]
            if self.load_parent_relationships
            else []
        )

        query = select(self.model).options(*query_options).offset(offset).limit(limit)
        executed_query = await db_session.execute(query)
        result = executed_query.scalars().all()

        return result

    async def query_on_joins(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single=False,
        options=None,
        order_by=None,
        join_conditions: Optional[List] = None,
        skip=0,
        limit=100,
    ) -> list[DBModelType]:
        # separate main model filters and joined table filters
        main_model_conditions = []
        join_conditions_filters = []

        for key, value in filters.items():
            if "." in key:
                # indicates a filter on a join table
                table_name, column_name = key.split(".")
                join_conditions_filters.append((table_name, column_name, value))
            else:
                # filter on the main model
                main_model_conditions.append(getattr(self.model, key) == value)
        query = select(self.model)

        # apply joins
        if join_conditions:
            for join_condition in join_conditions:
                query = query.join(*join_condition)

        # apply main model conditions
        query = query.filter(and_(*main_model_conditions))

        # Apply filters on joined tables
        for table_name, column_name, value in join_conditions_filters:
            join_model = None
            for join_condition in join_conditions:
                if join_condition[0].__name__ == table_name:
                    join_model = join_condition[0]
                    break
            if join_model:
                query = query.filter(getattr(join_model, column_name) == value)

        # check if options
        if options:
            query = query.options(*options)

        # check if order by
        if order_by:
            query = query.order_by(*order_by)

        query_result = await db_session.execute(query.offset(skip).limit(limit))

        return (
            query_result.unique().scalar_one_or_none()
            if single
            else query_result.unique().scalars().all()
        )

    async def query(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single=False,
        options=None,
        order_by=None,
    ) -> Union[List[DBModelType], None]:
        conditions = [getattr(self.model, k) == v for k, v in filters.items()]
        query = select(self.model).filter(and_(*conditions))

        # check if options
        if options:
            query = query.options(*options)

        # check if order by
        if order_by:
            query = query.order_by(*order_by)

        query_result = await db_session.execute(query)
        scalar_result = None if single else query_result.scalars().all()

        return query_result.scalar_one_or_none() if single else scalar_result

    async def query_count(self, db_session: AsyncSession):
        executed_query = await db_session.execute(
            select(func.count()).select_from(self.model)
        )
        count = executed_query.scalar()

        return count

    async def query_on_create(
        self,
        db_session: AsyncSession,
        filters: Dict[str, Any],
        single=False,
        options=None,
        create_if_not_exist=False,
    ):
        result = await self.query(
            db_session=db_session, filters=filters, single=single, options=options
        )

        if result:
            return result
        elif create_if_not_exist:
            db_obj = self.model(**filters)
            db_session.add(db_obj)

            return await self.commit_and_refresh(db_session=db_session, obj=db_obj)


class UpdateMixin(UtilsMixin):
    model: Type[DBModelType]

    async def update(
        self, db_session: AsyncSession, db_obj: DBModelType, obj_in: Dict[str, Any]
    ) -> DBModelType:
        for field, value in obj_in:
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db_session.add(db_obj)

        return await self.commit_and_refresh(db_session=db_session, obj=db_obj)


class DeleteMixin(UtilsMixin):
    model: Type[DBModelType]

    async def delete(
        self, db_session: AsyncSession, db_obj: DBModelType
    ) -> DBModelType:
        await db_session.delete(db_obj)
        await db_session.commit()


class DBOperations(CreateMixin, ReadMixin, UpdateMixin, DeleteMixin):
    def __init__(
        self,
        model: Generic[DBModelType],
        load_parent_relationships: bool = False,
        load_child_relationships: bool = False,
        excludes=[],
    ):
        self.model = model
        self.load_parent_relationships = load_parent_relationships
        self.load_child_relationships = load_child_relationships
        self.excludes = excludes
