from fastapi import FastAPI
from .routers import groups, expenses, balances
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(groups.router)
app.include_router(expenses.router)
app.include_router(balances.router)

@app.get("/")
def read_root():
    return {"message": "Splitwise Clone API"}