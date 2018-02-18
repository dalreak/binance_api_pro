import hmac
import hashlib
import urllib.request
import urllib
import time
import requests

ENDPOINT = "https://api.binance.com"
keyname={}

#key 입력
def set_key(apikey,secretkey):
    keyname['apikey'] =apikey
    keyname['secret'] =secretkey

#method : post,get,delete  path: 요청위치 params: 요청심볼
def signedRequest(method, path, params):
    query = urllib.parse.urlencode(sorted(params.items()))

    query += "&timestamp={}".format(int(time.time() * 1000))
    secret = bytes(keyname["secret"].encode("utf-8"))
    signature = hmac.new(secret, query.encode("utf-8"),
                         hashlib.sha256).hexdigest()
    query += "&signature={}".format(signature)
    resp = requests.request(method,
                            ENDPOINT + path + "?" + query,
                            headers={"X-MBX-APIKEY" : keyname['apikey']})
    data=resp.json()
    return data

#트레이딩 내역 가져오기
def get_tradelist(symbol):
    print("임시")



