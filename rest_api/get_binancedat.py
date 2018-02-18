'''
바이낸스에서 candle 자료를 읽어와 차트형태로 표현하는 코드
'''


from urllib.request import urlopen
import pandas as pd
import time
import matplotlib.pyplot as plt
import mpl_finance as mplf
import matplotlib.ticker as tck
import json
import numpy as np
import glob
import os


#binance candle api url
binanceURL="https://api.binance.com"

#바이낸스 캔들 데이터 사용 위한 클래스 호출시 symbol지정필요함
class get_candle_dat:
    def __init__(self,symbol):

#리스트 구성에 사용하기 위해 미리 호출
        self.Open=[]
        self.High=[]
        self.Low=[]
        self.Close=[]
        self.Date=[]
        self.name_list=[]
        self.binance_candle_df={}

#호출기호 생성위해 정의
        self.starttime=str((time.time()-2592000)*1000)[:-5]
        self.interval='1d'
        self.symbol=symbol

    def get_candle_dat(self):
#바이낸스 api이용해 특정 symbol candle 30일 데이터 받아오기
        binancecandlepage = urlopen(binanceURL+'/api/v1/klines'+'?symbol='+self.symbol+'&interval='+self.interval+'&startTime='+self.starttime)
        binancecandle=binancecandlepage.read().decode("utf-8")

# 받아온 데이터 list형태로 1차변환
        check_mklist = 0
        binancecandle = binancecandle[2:-3]
        binance_candle_list = binancecandle.split('],[')
        while check_mklist < 30:
            binance_candle_list[check_mklist] = binance_candle_list[check_mklist].split(',')
            check_mklist += 1


# binancecandle list 2차변
        def candle_mklist_append(num):
            i = 0
            list_temp = []
            if num == 0:
                while i < 30:
                    self.Date.append(time.strftime('%x', time.localtime(int(str(binance_candle_list[i][num])[:-3]))))
                    i += 1

            elif num == 1:
                while i < 30:
                    self.Open.append(binance_candle_list[i][num][1:-1])
                    i += 1

            elif num == 2:
                while i < 30:
                    self.High.append(binance_candle_list[i][num][1:-1])
                    i += 1

            elif num == 3:
                while i < 30:
                    self.Low.append(binance_candle_list[i][num][1:-1])
                    i += 1

            elif num == 4:
                while i < 30:
                    self.Close.append(binance_candle_list[i][num][1:-1])
                    i += 1

            else:
                print("wrong num")


        for i in [0, 1, 2, 3, 4]:
            candle_mklist_append(i)

# 데이터프레임 생성
        binance_candle_df = pd.DataFrame({'Date': self.Date, 'Open': self.Open, 'High': self.High, 'Close': self.Close, 'Low': self.Low},
                                 columns=['Date', 'Open', 'High', 'Low', 'Close'])
        self.binance_candle_df=binance_candle_df
        return binance_candle_df
    def show_candle_dat(self):

        for day in self.binance_candle_df['Date']:
            self.name_list.append(day[0:5])

# matplotlib 이용 캔들형태 출력
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)

        day_list = range(len(self.binance_candle_df))
        ax.xaxis.set_major_locator(tck.FixedLocator(day_list))
        ax.xaxis.set_major_formatter(tck.FixedFormatter(self.name_list))

        mplf.candlestick2_ohlc(ax, self.binance_candle_df['Open'], self.binance_candle_df['High'], self.binance_candle_df['Low'],
                               self.binance_candle_df['Close'], width=0.5, colorup='r', colordown='b')
        plt.show()

#바이낸스에서 데이터를 받아와 jsonfile폴더에 저장하는 함수
def get_binancedat():
    filename=os.getcwd()
    filename=filename + '/rest_api/jsonfile/'+str(int(time.time()))+".json"
    binancedatURL = "https://api.binance.com/api/v1/ticker/24hr"
    dict_del_source = ['prevClosePrice', 'weightedAvgPrice', 'lastQty', 'bidQty', 'openPrice', 'quoteVolume', 'firstId',
                       'lastId', 'count']

    # 바이낸스 api이용 모든 시세 가져오기 1분 1200limit
    binancedatpage = urlopen(binancedatURL)
    binancedat = json.loads(binancedatpage.read().decode("utf-8"))

    # json 파일 생성
    makejson = {}
    for transdict in binancedat:
        if (transdict['symbol'][-3:] != 'BTC'):
            pass
        else:
            for dict_del in dict_del_source:
                del transdict[dict_del]
            makejson[transdict['symbol']] = transdict


    jsonoutput = makejson
    with open(filename, 'w', encoding="utf-8") as make_json_file:
        json.dump(jsonoutput, make_json_file, ensure_ascii=False, indent="\t")
    dir_list = glob.glob(os.getcwd()+"/rest_api/jsonfile/*")
    if(len(dir_list)>15840):
        num=len(dir_list)>15840
        delet_dir_list=dir_list[:num+1]
        for i in delet_dir_list:
            os.unlink(os.getcwd()+"/rest_api/jsonfile/"+i+".json")
    time.sleep(20)

#시세데이터에서 상위 10개 종목 바 형태로 표시하는 함수
def get_binancedat_bar():
    i = 1
    crypto = []
    fluctuations = []

# 가장 최근에 생성된 json 파일 불러오기

    dir_list = glob.glob(os.getcwd()+"/rest_api/jsonfile/*")
    dir_list.sort()

    f = open(dir_list[-1]).read()
    binance_mkbar_dat = json.loads(f)

# 불러온 json 데이터에서 가격변동률을 알아와 상위 10개 뽑는것
    compare_tpt = [binance_mkbar_dat[key_lists]['priceChangePercent'] + '|' + binance_mkbar_dat[key_lists]['symbol'] for
                   key_lists in binance_mkbar_dat.keys()]

    return compare_tpt
# 바형태 그래프 그리는 것
def show_binancebar(compare_tpt):
    i = 1
    crypto = []
    fluctuations = []
    def caldigit(n):
        return float(n.split('|')[0])

    compare_tpt = sorted(compare_tpt, key=caldigit)

    while i < 11:
        fluctuations.append(float(compare_tpt[-i].split('|')[0]))
        crypto.append(compare_tpt[-i].split('|')[1])
        i += 1

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)

    ypos = np.arange(10)
    rects = plt.barh(ypos, fluctuations, align='center', height=0.5)
    plt.yticks(ypos, crypto)

    plt.xlabel(' pricechangepercent ')
    plt.show()

