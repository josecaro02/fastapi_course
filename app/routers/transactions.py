from fastapi import APIRouter, HTTPException, status
from models import Transaction, TransactionCreate, Customer
from db import SessionDep
from sqlmodel import select

router = APIRouter()

@router.post('/transactions', tags=['Transactions'])
async def create_transactions(transaction_data: TransactionCreate, session : SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get('customer_id'))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@router.get('/transactions', tags=['Transactions'])
async def list_transactions(session : SessionDep):
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions