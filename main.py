from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates

d = datetime.today().day
m = datetime.today().month
y = datetime.today().year

start = datetime(y-1, m, d)
end = datetime(y, m, d)


class Broker:
    @classmethod
    def find_peak(cls, df):
        return df['Open'].max()

    @classmethod
    def build_candle(cls, tik):
        yf.pdr_override()
        app.get_news(tik)
        ohlc = pdr.get_data_yahoo(tik, start=datetime(y-3, m, d), end=datetime(y, m, d), interval="1mo")
        dates = ohlc.index
        ohlc['Dates'] = dates
        plt.style.use('ggplot')
        # Extracting Data for plotting
        ohlc = ohlc.loc[:, ['Dates', 'Open', 'High', 'Low', 'Close']]
        ohlc['Dates'] = pd.to_datetime(ohlc['Dates'])
        ohlc['Dates'] = ohlc['Dates'].apply(mpl_dates.date2num)
        ohlc = ohlc.astype(float)
        Broker.find_peak(ohlc)
        # Creating Subplots
        fig, ax = plt.subplots()
        candlestick_ohlc(ax, ohlc.values, width=10, colorup='green', colordown='red', alpha=0.8)
        # Setting labels & titles
        ax.set_xlabel('Dates')
        ax.set_ylabel('Price')
        fig.suptitle(f'Daily Candlestick Chart of ${tik}')
        # Formatting Date
        date_format = mpl_dates.DateFormatter('%d-%m-%Y')
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        fig.tight_layout()
        ohlc['SMA5'] = ohlc['Close'].rolling(1).mean()
        ax.plot(ohlc['Dates'], ohlc['SMA5'], color='green', label='SMA5')
        plt.legend()
        plt.show()

    @staticmethod
    def get_news(tik):
        import requests
        url = "https://stock-market-data.p.rapidapi.com/stock/buzz/news"
        querystring = {"ticker_symbol":f"{tik}","date":"2021-3-1"}
        headers = {
            'x-rapidapi-key': "11d8bc37d8mshf186de22a127423p1552c3jsnd379e8ad19aa",
            'x-rapidapi-host': "stock-market-data.p.rapidapi.com"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()
        news = response['news']
        for i in news:
            for j in i.keys():
                if j == "title":
                    print(i['title'] + "\n")



app = Broker
app.build_candle(input("Choose your destiny: "))

##TODO сделать модель для тренда цены
##TODO (через верхнюю и нижнюю границу, возможно, с помощью углов наклона "пола" и "потолка")