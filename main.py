from fastapi import FastAPI
from datetime import datetime
import zoneinfo
from models import Customer, CustomerCreate, Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select

app=FastAPI(lifespan=create_all_tables)


     
country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

db_customers: list[Customer] = []

@app.get('/')
async def root():
    return {"message": "hola mundo"}

@app.get('/time/{iso_code}')
async def time(iso_code:str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz=zoneinfo.ZoneInfo(timezone_str)
    print(tz)
    return {"time": datetime.now(tz)}

@app.post('/customers', response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get('/customers', response_model=list[Customer])
async def get_customers(session:SessionDep):
    return session.exec(select(Customer)).all()

@app.post('/transactions')
async def create_transactions(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices')
async def create_invoices(invoice_data: Invoice):
    return invoice_data