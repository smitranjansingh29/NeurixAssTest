from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    user_ids: List[int]

class Group(GroupBase):
    id: int
    users: List[User]
    class Config:
        orm_mode = True

class ExpenseSplitBase(BaseModel):
    user_id: int
    amount: Optional[float] = None
    percentage: Optional[float] = None

class ExpenseBase(BaseModel):
    description: str
    amount: float
    paid_by: int
    split_type: str

class ExpenseCreate(ExpenseBase):
    splits: List[ExpenseSplitBase]

class Expense(ExpenseBase):
    id: int
    group_id: int
    class Config:
        orm_mode = True

class Balance(BaseModel):
    user_id: int
    amount: float

class ChatQuery(BaseModel):
    query: str