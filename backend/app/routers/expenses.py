from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import get_db

router = APIRouter(prefix="/groups/{group_id}/expenses")

@router.post("/", response_model=schemas.Expense)
def create_expense(
    group_id: int, 
    expense: schemas.ExpenseCreate, 
    db: Session = Depends(get_db)
):
    try:
        return crud.create_expense(db, expense, group_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))