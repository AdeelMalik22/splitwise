from datetime import datetime

from pydantic import BaseModel


class CreateGroupRequestSchema(BaseModel):
    name: str
    description: str

class RetrieveGroupRequestSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class AddUserInGroupRequestSchema(BaseModel):
    user_id: int
    group_id: int