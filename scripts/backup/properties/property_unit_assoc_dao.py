# daos
from app.dao.resources.base_dao import BaseDAO

# models
from app.models.property_unit_assoc import PropertyUnitAssoc


class PropertyUnitAssocDAO(BaseDAO[PropertyUnitAssoc]):
    def __init__(self):
        self.model = PropertyUnitAssoc

        super().__init__(self.model)
