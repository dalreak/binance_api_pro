from rest_api import get_binanceuserdat
from rest_api import get_binancedat
import threading

print("안녕하세요 이 프로그램은 자동 트레이딩 봇입니다")
print("이 프로그램을 사용하기전 binance.com에서 apikey와 secretkey를 받으시기 바랍니다")
print("그럼 apikey와 secretkey를 입력해 주시기 바랍니다")
temp=input("apikey를 입력해 주세요")
temp1=input("secretkey를 입력해 주세요")
get_binanceuserdat.set_key(temp,temp1)

for i in [1]:
    t=threading.Thread(target=get_binancedat.get_binancedat())
    t.daemon = True
    t.start()

for i in [1]:
    print('hello')
