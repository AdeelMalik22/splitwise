from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from app.api.expenses.model import Expenses
from app.api.expenses.schema.request import CreateExpenseRequestSchema
from app.api.expenses.settlements import get_settlements_for_group
from app.utils.auth import get_current_user
from app.utils.database_connections import get_db

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/create/expense")
def create_expense(expense: CreateExpenseRequestSchema,db:Session = Depends(get_db)):
    expense = Expenses(name=expense.name, description=expense.description, amount=expense.amount,paid_by=expense.paid_by,split_on=expense.split_on,group_id=expense.group_id)
    db.add(expense)
    db.commit()
    return {"message":"Expense Created"}


@router.get("/{group_id}/settlements")
def get_settlements(group_id:int,db:Session = Depends(get_db),user = Depends(get_current_user)):
    expenses = db.query(Expenses).filter(Expenses.group_id == group_id).all()
    settlements = get_settlements_for_group(expenses,user[1],db)
    return settlements


@router.post("/{group_id}/payback")
def payback_to_user():
    pass