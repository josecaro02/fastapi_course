from fastapi import APIRouter, HTTPException, Query, status
from models import Customer, CustomerCreate, CustomerPlan, CustomerUpdate, Plan, StatusEnum
from db import SessionDep
from sqlalchemy import select

router = APIRouter()

@router.post('/customers', response_model=Customer, tags=['Customers'])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    print(customer)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    print(customer)
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
    customers =  session.exec(select(Customer)).scalars().all()
    print(customers)
    return customers

@router.post('/customers/{customer_id}/plans/{plan_id}', tags=['Customers'])
async def subscribe_customer_to_plan(
        customer_id: int, plan_id: int,session: SessionDep,
        plan_status: StatusEnum = Query()
        ):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The customer of plan doesn\'t exist'
            )
    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db

@router.get('/customers/{customer_id}/plans', tags=['Customers'])
async def get_plans_by_customer(
                customer_id: int, session: SessionDep,
                plan_status: StatusEnum = Query()
            ):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The customer doesn\t exist'
        )
    query = select(CustomerPlan)\
        .where(CustomerPlan.customer_id == customer_id)\
        .where(CustomerPlan.status == plan_status )
    
    plans = session.exec(query).scalars().all()
    print(plans)
    return plans
