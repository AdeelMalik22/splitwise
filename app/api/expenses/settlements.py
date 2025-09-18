from collections import defaultdict
from sqlalchemy.orm import Session
from app.api.users.models import User


def get_username(uid, db):
    user = db.query(User).filter(User.id == uid).first()
    return user.username if user else f"User {uid}"


def get_settlements_for_group(expenses, user_id, db: Session):
    balance = defaultdict(float)

    for expense in expenses:
        total_amount = expense.amount
        payers = expense.paid_by or []
        splitters = expense.split_on or []

        if not payers or not splitters:
            continue

        num_payers = len(payers)
        num_splitters = len(splitters)

        owed_share = total_amount / num_splitters

        for splitter in splitters:
            for payer in payers:
                if splitter == payer:
                    continue
                split_amount = owed_share / num_payers

                if splitter == user_id:
                    balance[payer] -= split_amount  # user owes others
                elif payer == user_id:
                    balance[splitter] += split_amount  # others owe user

    response = {
        "You need to pay": [],
        "you will get": []
    }

    for uid, net_amount in balance.items():
        rounded_amount = round(abs(net_amount), 2)
        username = get_username(uid, db)

        if net_amount < 0:
            response["You need to pay"].append({
                "to_user": username,
                "amount": rounded_amount
            })
        elif net_amount > 0:
            response["you will get"].append({
                "from_user": username,
                "amount": rounded_amount
            })

    return response
