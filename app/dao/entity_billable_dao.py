from app.dao.base_dao import BaseDAO
from app.models.entity_billable import EntityBillable

class EntityBillableDAO(BaseDAO[EntityBillable]):
    def __init__(self):
        self.model = EntityBillable

        super().__init__(self.model)