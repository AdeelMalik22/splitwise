from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from .models import Groups, UsersGroups

from app.api.groups.schema.request import CreateGroupRequestSchema, RetrieveGroupRequestSchema, \
    AddUserInGroupRequestSchema
from app.utils.database_connections import get_db
from ..expenses.model import Expenses
from ..expenses.schema.request import GetExpenseRequestSchema
from ..users.models import User

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/expense_list/{group_id}", response_model=List[GetExpenseRequestSchema])
def get_expense_list(group_id: int, db: Session = Depends(get_db)):
    expenses = db.query(Expenses).filter(Expenses.group_id == group_id).all()
    response = []

    for expense in expenses:
        paid_by_usernames = []
        for user_id in expense.paid_by:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                paid_by_usernames.append(user.username)

        split_on_usernames = []
        for user_id in expense.split_on:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                split_on_usernames.append(user.username)

        response.append({
            "name": expense.name,
            "description": expense.description,
            "amount": expense.amount,
            "paid_by": paid_by_usernames,
            "split_on": split_on_usernames,
            "per_person":expense.amount/len(split_on_usernames),
        })

    return response


@router.post("/create")
def create_group(request:CreateGroupRequestSchema,db:Session= Depends(get_db)):
    groups =Groups(name=request.name, description=request.description)
    db.add(groups)
    db.commit()
    return {"status":"success", "message":"Group created"}

@router.get("/groups",response_model=List[RetrieveGroupRequestSchema])
def get_groups(db:Session= Depends(get_db)):
    return db.query(Groups).all()


@router.post("/add_user")
def add_user_in_group(request:AddUserInGroupRequestSchema,db:Session= Depends(get_db)):
    existing_user = db.query(UsersGroups).filter(UsersGroups.user_id == request.user_id,UsersGroups.group_id==request.group_id ).first()
    if existing_user:
        return {"message":"User already in the group"}
    add_user = UsersGroups(user_id=request.user_id,group_id=request.group_id)
    db.add(add_user)
    db.commit()
    return {"status":"success", "message":"User added"}

@router.get("/user/{group_id}")
def get_user_by_user_id(group_id:int,db:Session= Depends(get_db)):
    groups_ids =db.query(UsersGroups).filter(UsersGroups.group_id == group_id ).all()
    group_user = []
    if groups_ids:
        for ids in groups_ids:
            groups = db.query(User).filter(User.id == ids.user_id).first()
            group_user.append(groups)
    return group_user


@router.delete("/{group_id}/{user_id}")
def delete_user_by_user_id(user_id:int,group_id:int,db:Session= Depends(get_db)):
    remove_user = db.query(UsersGroups).filter(UsersGroups.user_id == user_id,UsersGroups.group_id==group_id).first()
    if remove_user:
        db.delete(remove_user)
        db.commit()
        return {"status":"success", "message":"User deleted"}
    return {"status":"failure", "message":"User does not exist"}

