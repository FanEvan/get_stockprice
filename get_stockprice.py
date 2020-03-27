# -*- coding: utf-8 -*-
import requests,datetime
import pandas as pd
import matplotlib.pyplot as plt

def get_ohlc(twse_ticker):
    today= datetime.datetime.today().strftime("%Y%m%d")
    twse_url="https://www.twse.com.tw/exchangeReport/STOCK_DAY?\
    response=json&date={}&stockNo={}".format(today,twse_ticker)
    stock=requests.get(twse_url).json()
    trading_dates=[]
    opens=[]
    highs=[]
    lows=[]
    closes=[]
    for i in range(len(stock["data"])):
        trading_dates.append(stock["data"][i][0])
        opens.append(float(stock["data"][i][3]))
        highs.append(float(stock["data"][i][4]))
        lows.append(float(stock["data"][i][5]))
        closes.append(float(stock["data"][i][6]))
    
    trading_dates_year= [str(int(td.split("/")[0])+1911) for td in trading_dates]
    trading_dates_month= [td.split("/")[1] for td in trading_dates]
    trading_dates_day= [td.split("/")[2] for td in trading_dates]
    trading_dates=["{}/{}".format(m,d) for m, d \
                   in zip(trading_dates_month,trading_dates_day)]
    df=pd.DataFrame()
    df["trading_date"]=trading_dates
    df["opens"]=opens
    df["highs"]=highs
    df["lows"]=lows
    df["closes"]=closes
    df = df.set_index("trading_date")
    return df

def main():
    company_code= input("輸入4碼股票代碼")
    tsmc = get_ohlc(company_code)
    print(tsmc)
    
    
    if tsmc["opens"][-1] < 7.00:
        print("建議: 馬上進場!!!")
    else:
        print("建議: 繼續等待...")
        
    plt.plot(tsmc["opens"])
    plt.title("Open Price on date")
    plt.xlabel("Dates")
    plt.ylabel("Prices")
    plt.show()


if __name__ == "__main__":
    main()
    