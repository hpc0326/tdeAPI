from pydantic import BaseModel
from typing import List
import requests as rq
import configparser
import base64
import hashlib
import hmac
import uuid
import json

config = configparser.ConfigParser()
config.read('./module/config.ini')


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

def createSignature(nonce, order, uri):

    body = config['data']['LINEPAY_CHANNEL_SECRET_KEY'] + uri + order + nonce

    encrypt = hmac.new(str.encode(config['data']['LINEPAY_CHANNEL_SECRET_KEY']),
                str.encode(body),
                digestmod= hashlib.sha256).digest()
    signature = base64.b64encode(encrypt).decode("utf-8")
    return signature

def linepay(order):
    nonce = str(uuid.uuid4())
    uri = f"/{config['data']['LINEPAY_VERSION']}/payments/request"
    url = f"{config['uri']['LINEPAY_SITE']}{config['data']['LINEPAY_VERSION']}/payments/request"

    """order = {
        "amount" : 100,
        "currency" : "TWD",
        "orderId" : nonce,
        "packages": [{
            "id": "12345",
            "amount" : 100,
            "name" : 'animal',
            "products" :[{
                "name": "beans",
                "quantity" : 1,
                "price" : 100
        }]
        }],
        "redirectUrls" : {
            "confirmUrl" : 'http://localhost:3000/LPConfirm',
            "cancelUrl" : 'http://localhost:3000/LPFailed'
        }
    }"""

    json_order = json.dumps(order)

    header = {
        "Content-Type" : 'application/json',
        "X-LINE-ChannelId" : config['data']['LINEPAY_CHANNEL_ID'],
        "X-LINE-Authorization-Nonce" : nonce,
        "X-LINE-Authorization" : createSignature(nonce, json_order, uri)
    }

    response = rq.post(url, headers = header, data = json_order)
    response = json.loads(response.content)
    print(response)
    back = {
        'returnCode' : response['returnCode'],
        'web_url' : str(response['info']['paymentUrl']['web']),
        'transaction_id' : str(response['info']['transactionId'])
    }
    

    if response['returnCode'] == "0000":
        info = response['info']
        web_url = info['paymentUrl']['web']
        transaction_id = str(info['transactionId'])
        #print(f"付款web_url:{web_url}")
        print(f"request0000 :{transaction_id}")

    return back

def confirm(transaction, body):
    nonce = str(uuid.uuid4())
    json_body = json.dumps(body)
    url = f"{config['uri']['LINEPAY_SITE']}{config['data']['LINEPAY_VERSION']}/payments/{transaction}/confirm"
    uri = f"/{config['data']['LINEPAY_VERSION']}/payments/{transaction}/confirm"

    header = {
        "Content-Type" : 'application/json',
        "X-LINE-ChannelId" : config['data']['LINEPAY_CHANNEL_ID'],
        "X-LINE-Authorization-Nonce" : nonce,
        "X-LINE-Authorization" : createSignature(nonce, json_body, uri)
    }

    response = rq.post(url, headers = header, data = json_body)
    response = json.loads(response.content)
    
    back = {
        'returnCode' : response['returnCode']
    }
    if response['returnCode'] == "0000":
        info = response['info']
        transaction_id = str(info['transactionId'])
        print(f'confirm 0000 : {transaction}')

    return back


