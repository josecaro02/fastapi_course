from fastapi import APIRouter, HTTPException, status
from models import Customer, CustomerCreate, CustomerUpdate
from db import SessionDep
from sqlalchemy import select

router = APIRouter()

@router.post('/customers', response_model=Customer, tags=['Customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get('/customer/{customer_id}', response_model=Customer, tags=['Customers'])
async def read_customer(customer_id:int, session:SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer doesn\'t exist' )
    return customer_db

@router.delete('/customer/{customer_id}', tags=['Customers'])
async def delete_customer(customer_id:int, session:SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer doesn\'t exist' )
    session.delete(customer_db)
    session.commit()
    return  {'detail': 'OK'}

@router.patch('/customer/{customer_id}', response_model=Customer, status_code=status.HTTP_201_CREATED, tags=['Customers'])
async def read_customer(customer_id:int, customer_data: CustomerUpdate, session:SessionDep):
    customer_db = session.get(Customer, customer_id)
    if customer_db is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer doesn\'t exist' )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@router.get('/customers', response_model=list[Customer], tags=['Customers'])
async def get_customers(session:SessionDep):
    return session.exec(select(Customer)).all()