#dependencies
from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from typing import List
import os
import shutil
from pydantic import BaseModel

#source
from module import he, elevator, linepay
from module.Data.data import dataWriter
from module.Map.returnMap import deleteFolder, getFile, produceMap

app = FastAPI()
origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#format for linepay
class Product(BaseModel):
    name : str
    quantity : int
    price : int

class Redirect(BaseModel):
    confirmUrl : str
    cancelUrl : str

class Package(BaseModel):
    id : str
    amount: int
    name : str
    products : List[Product]


class Order(BaseModel) :
    amount : int
    currency : str
    orderId : str
    packages: List[Package]
    redirectUrls : Redirect

class Trans(BaseModel):
    amount : int
    currency : str
    

#elevator API
@app.get("/elevator")
def read_root():
    return elevator.elevator_response()


#excel data API
@app.post('/finances/{storename}/')
def function(storename : str , start = None , end =  None ):
    return dataWriter(storename , start , end)


#linepay API
@app.post('/linepay/request/')
def read_root(order : Order):
    json_data_order = jsonable_encoder(order)
    print('request')
    return linepay.linepay(json_data_order)
    
@app.post('/linepay/confirm/{transaction}/')
def read_root(transaction:str, body : Trans):
    json_body = jsonable_encoder(body)
    print('confirm')
    return linepay.confirm(transaction, json_body)


#map sketching, receiving API

#for deliver to finish the order
@app.get('/del/{orderID}/')
def read_root(orderID:str):
    return deleteFolder(orderID)

#for consumer and deliver
@app.get('/get/{orderID}/{picType}/')
def read_root(orderID:str, picType:str):
    return getFile(orderID, picType)
    

#for deliver
@app.get('/info/{orderID}/')
def read_root(start : int = None , end : str = None, deliver : str = None , orderID : str = None):
    return produceMap(start, end, deliver, orderID)
    #return good

