from fastapi import APIRouter, HTTPException, Query, status
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
async def list_transactions(
    session : SessionDep,
    skip: int = Query(0, description='Registros a omitir/desde donde comienza'),
    limit: int = Query(10, description='Número de registros')
    ):
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()
    return transactions