import requests
import json
from time import *
import time
import pandas as pd
import alice_blue
from alice_blue import *
from login import *
import login

access_token=AliceBlue.login_and_get_access_token(username=usn,password=psw,twoFA=twoFA,api_secret=api_secret)
alice= AliceBlue(username=usn,password=psw,access_token=access_token, master_contracts_to_download=['NSE', 'BSE','MCX'])

exchange= input("Please enter exchange:").upper()
symbol=input("Please enter Symbol:").upper()
tokens= alice.get_instrument_by_symbol(exchange,symbol)
script=json.dumps(tokens)
script_det=json.loads(script)
script_token= script_det[1]
strt_time= 1598941814
timenw=int(time.time())
cand_time= 5
data_typ=input("Please enter feed type live/ historical:").lower()
print(exchange,symbol,data_typ)


access_token_hist='YOUR X-AUTH TOKEN HERE'

headers = {
    'authority': 'ant.aliceblueonline.com',
    'accept': '*/*',
    'x-authorization-token': access_token_hist ,
    'x-requested-with': 'XMLHttpRequest',
}

params = f'exchange={exchange}&token={script_token}&candletype=1&starttime={strt_time}&endtime={timenw}&type={data_typ}&data_duration={cand_time}'


response = requests.get('https://ant.aliceblueonline.com/api/v1/charts', headers=headers, params=params)
jso= response.text
conv= json.loads(jso)
datas= conv['data']

feeddata=[]
for data in datas:
    sec=data[0]
    t= time.ctime(sec)
    opn= data[1]/100
    hig=data[2]/100
    lo=data[3]/100
    clo= data[4]/100
    vol=data[5]
    feed={"time":t,"open":opn,"high":hig,"low":lo,"close":clo,"volume":vol}
    feeddata.append(feed)  

datafm=pd.DataFrame(feeddata)

print(datafm)

