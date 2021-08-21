from pandas_datareader import data as pdr
import yfinance as yf # this lib is free
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mpl_dates
from candles import WorkingFunctions


M = datetime.today().minute
h = datetime.today().hour
d = datetime.today().day
m = datetime.today().month
y = datetime.today().year

start = datetime(y-1, m, d)
end = datetime(y, m, d)

class Broker:
    @staticmethod
    def form_data(tik): # could use 12Data if was rich enough
        yf.pdr_override()
        ohlc = pdr.get_data_yahoo(tickers=tik,
                                  period="30m",
                                  interval="1m")
        dates = ohlc.index
        ohlc = ohlc.astype(float)
        ohlc['Dates'] = dates.to_pydatetime()
        plt.style.use('ggplot')
        # Extracting Data for plotting
        ohlc = ohlc.loc[:, ['Dates', 'Open', 'High', 'Low', 'Close']]
        ohlc['Dates'] = pd.to_datetime(ohlc['Dates'])
        ohlc['Dates'] = ohlc['Dates'].apply(mpl_dates.date2num)
        # print(ohlc)
        return ohlc

    dataframe = None




    design_candle = {}

    design_candle['type'] = "candle"
    design_candle['style'] = "charles"
    design_candle['show_notrading'] = False
    design_candle['mav'] = 3
    design_candle['volume'] = True

    @staticmethod
    def get_news(tik):
        import requests
        url = "https://stock-market-data.p.rapidapi.com/stock/buzz/news"
        querystring = {"ticker_symbol":f"{tik}","date":f"{y}-{m}-{d}"}
        headers = {
            'x-rapidapi-key': "11d8bc37d8mshf186de22a127423p1552c3jsnd379e8ad19aa",
            'x-rapidapi-host': "stock-market-data.p.rapidapi.com"
            }
        response = requests.get(url, headers)
        response = response.json()
        news = response['news']
        for i in news:
            for j in i.keys():
                if j == "title":
                    print(i['title'] + "\n")
