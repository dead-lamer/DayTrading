from pandas_datareader import data as pdr
import yfinance as yf # this lib is free
from datetime import datetime
import matplotlib.pyplot as plt

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
                                  period="4d", # []
                                  interval="1h") # [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
        ohlc = ohlc.astype(float)
        plt.style.use('ggplot')
        # Extracting Data for plotting
        ohlc = ohlc.loc[:, ['Open', 'High', 'Low', 'Close']]
        # print(ohlc)
        return ohlc

    dataframe = None




    design_candle = {}

    design_candle['type'] = "candle"
    design_candle['style'] = "charles"
    design_candle['show_notrading'] = False
    design_candle['mav'] = 2
    design_candle['volume'] = True

    @staticmethod
    def get_news(tik):
        import requests
        url = "https://stock-market-data.p.rapidapi.com/stock/buzz/news"
        querystring = {"ticker_symbol":f"{tik}","date":f"{y}-{m}-{d}"}
        headers = {
            'x-rapidapi-key': "",
            'x-rapidapi-host': "stock-market-data.p.rapidapi.com"
            }
        response = requests.get(url, headers)
        response = response.json()
        news = response['news']
        for i in news:
            for j in i.keys():
                if j == "title":
                    print(i['title'] + "\n")
