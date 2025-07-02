from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db

router = APIRouter()

@router.get("/groups/{group_id}/balances", response_model=list[schemas.Balance])
def get_group_balances(group_id: int, db: Session = Depends(get_db)):
    balances = crud.get_balances(db, group_id)
    if balances is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return balances

@router.get("/users/{user_id}/balances")
def get_user_balances(user_id: int, db: Session = Depends(get_db)):
    balances = crud.get_user_balances(db, user_id)
    if balances is None:
        raise HTTPException(status_code=404, detail="User not found")
    return balances