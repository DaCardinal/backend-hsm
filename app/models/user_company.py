from sqlalchemy import Column, ForeignKey, UUID

from app.models.model_base import BaseModel

class UsersCompany(BaseModel):
    __tablename__ = 'users_company'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey('company.company_id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))