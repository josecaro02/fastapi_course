from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status
from datetime import datetime
import zoneinfo

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import Customer, Transaction, Invoice
from db import  create_all_tables
from .routers import customers, transactions, invoices, plans
import time

app=FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)

@app.middleware('http')
async def log_request_time(request: Request, call_next ):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f'  -Request: {request.url}\n -Completado en: {process_time:.4f} secs')
    return response
     
country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

db_customers: list[Customer] = []

security = HTTPBasic()

@app.get('/')
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    print(credentials)
    if credentials.username == 'holi' and credentials.password == 'holi': 
        return {"message": f'Hola {credentials.username}'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get('/time/{iso_code}')
async def get_time_by_iso(iso_code:str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz=zoneinfo.ZoneInfo(timezone_str)
    print(tz)
    return {"time": datetime.now(tz)}


