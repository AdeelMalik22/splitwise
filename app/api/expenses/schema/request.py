from pydantic import BaseModel


class CreateExpenseRequestSchema(BaseModel):
    name:str
    description:str
    amount:int
    group_id:int
    paid_by:list[int]
    split_on:list[int]


class GetExpenseRequestSchema(BaseModel):
    name:str
    description:str
    amount:int
    paid_by:list[str]
    split_on:list[str]
    per_person:float