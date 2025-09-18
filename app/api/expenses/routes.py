from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from app.api.expenses.model import Expenses
from app.api.expenses.schema.request import CreateExpenseRequestSchema
from app.utils.database_connections import get_db

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/create/expense")
def create_expense(expense: CreateExpenseRequestSchema,db:Session = Depends(get_db)):
    expense = Expenses(name=expense.name, description=expense.description, amount=expense.amount,paid_by=expense.paid_by,split_on=expense.split_on,group_id=expense.group_id)
    db.add(expense)
    db.commit()
    return {"message":"Expense Created"}

