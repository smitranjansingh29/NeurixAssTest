from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    # Add users to group
    for user_id in group.user_ids:
        user = get_user(db, user_id)
        if user:
            db_group.users.append(user)
    
    db.commit()
    db.refresh(db_group)
    return db_group

def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def create_expense(db: Session, expense: schemas.ExpenseCreate, group_id: int):
    db_expense = models.Expense(
        **expense.dict(exclude={"splits"}),
        group_id=group_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    # Calculate splits
    if expense.split_type == "equal":
        num_users = len(db_expense.group.users)
        share = expense.amount / num_users
        for user in db_expense.group.users:
            db_split = models.ExpenseSplit(
                expense_id=db_expense.id,
                user_id=user.id,
                amount=share
            )
            db.add(db_split)
    
    elif expense.split_type == "percentage":
        total_percentage = sum(split.percentage for split in expense.splits)
        if total_percentage != 100:
            raise ValueError("Total percentage must be 100")
        
        for split in expense.splits:
            amount = (expense.amount * split.percentage) / 100
            db_split = models.ExpenseSplit(
                expense_id=db_expense.id,
                user_id=split.user_id,
                amount=amount,
                percentage=split.percentage
            )
            db.add(db_split)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_balances(db: Session, group_id: int):
    group = get_group(db, group_id)
    if not group:
        return None
    
    balances = {}
    
    # Initialize balances
    for user in group.users:
        balances[user.id] = 0.0
    
    # Calculate balances
    for expense in group.expenses:
        paid_by = expense.paid_by
        for split in expense.splits:
            balances[paid_by] += split.amount
            balances[split.user_id] -= split.amount
    
    return [{"user_id": k, "amount": v} for k, v in balances.items()]

def get_user_balances(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None
    
    balances = []
    
    for group in user.groups:
        group_balances = get_balances(db, group.id)
        for balance in group_balances:
            if balance["user_id"] == user.id:
                balances.append({
                    "group_id": group.id,
                    "group_name": group.name,
                    "amount": balance["amount"]
                })
    
    return balances