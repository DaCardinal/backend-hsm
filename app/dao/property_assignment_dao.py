from app.dao.base_dao import BaseDAO
from app.models import PropertyAssignment

class PropertyAssignmentDAO(BaseDAO[PropertyAssignment]):
    def __init__(self, excludes = [], nesting_degree : str = BaseDAO.NO_NESTED_CHILD):
        self.model = PropertyAssignment
        self.primary_key = "property_assignment_id"

        super().__init__(self.model, nesting_degree = nesting_degree, excludes=excludes)