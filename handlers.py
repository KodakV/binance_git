import requests as r
import os.path
import signature
from binance_config import headers
from binance_config import secret_key
from urllib.parse import urlencode
import time

symbol='ETHUSDT'
root_url='https://api.binance.com'
# response=r.get(os.path.join(root_url+'/api/v3/ping'))


def getServTime():
    return r.get(root_url+'/api/v3/time').json()['serverTime']
def getTime():
    return int(time.time()*1000)
def getSystemStatus():
    return r.get(root_url +'/sapi/v1/system/status').json()

def orderBook(symbol,count='All'):
    if count=='All':
        return r.get(root_url+'/api/v3/depth', params={'symbol':symbol}).json()
    else:
        result =r.get(root_url+'/api/v3/depth', params={'symbol':symbol}).json()
        result['bids']=result['bids'][0:count]
        result['asks']=result['asks'][0:count]
        return result
def allCoinsWallet():
    url_patch="/sapi/v1/capital/config/getall"
    timestamp=getServTime()
    payload = {
        "recvWindow":5000,
        "timestamp":timestamp
    }

    query_string=urlencode(payload,True)
    signature=hash.signature(secret_key,query_string)
    url=root_url+url_patch+'?'+query_string+"&signature="+signature
    resp=r.get(url, headers=headers)
    return resp.json()
#Получить данные обо всех монетах в кошельке
def getSpotCoins():
    url_patch="/sapi/v3/asset/getUserAsset"
    timestamp=getServTime()
    payload = {
        "timestamp":timestamp
    }
    query_string=urlencode(payload,True)
    signature=hash.signature(secret_key,query_string)
    url=root_url+url_patch+'?'+query_string+"&signature="+signature
    resp=r.post(url=url,headers=headers)
    return resp.json()
#   Получение информации о всех парах
def getAllInfo():
    url_patch="/api/v3/exchangeInfo"
    resp=r.get(root_url+url_patch,headers=headers)
    return resp.json()
# Получение информации о всех символах пар
def getAllSymbols():
    info=getAllInfo()
    symbols=[]
    for i in range(len(info['symbols'])):
        symbols.append(info['symbols'][i]['symbol'])
    return symbols
symbols=getAllSymbols()

# Получение свечного графиика
def getKline(symbol,interval,limit):
    url_patch='/api/v3/klines'

    payload = {
        "symbol": symbol,
        "interval": interval,
        "limit" : limit
    }
    query_string=urlencode(payload,True)
    resp=r.get(root_url+url_patch+"?"+query_string,headers=headers)
    return resp.json()


# def bestOffer(symbol):
#     offers=orderBook(symbol)
#     bestAsk=offers['asks'][0]
#     bestBid=offers['bids'][0]
#     spread=float(bestAsk[0])-float(bestBid[0])
#     return (bestBid[0],bestAsk[0], spread)

# def send_signed_requests:
# def send_requests:
def createOrder(symbol,side, types,quantity,price):
    url_patch='/api/v3/order'
    timestamp=getServTime()

    payload = {
        "symbol": "SOLBUSD",
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": quantity,
        "price": price,
        "timestamp":timestamp
    }

    query_string=urlencode(payload,True)
    signature=hash.signature(secret_key,query_string)
    url=root_url+url_patch+'?'+query_string+"&signature="+signature
    resp=r.post(url, headers=headers)
    return resp.text

