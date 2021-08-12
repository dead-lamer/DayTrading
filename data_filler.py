from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mpl_dates
from datetime import datetime
from main import get_ticker



class DataMaker:


    ticker = get_ticker()

    d = datetime.today().day
    m = datetime.today().month
    y = datetime.today().year
    start = datetime(y - 1, m, d)
    end = datetime(y, m, d)

    @staticmethod
    def form_data():
        ohlc = pdr.get_data_yahoo(tickers=DataMaker.ticker,
                                  period="10m",
                                  interval="1m")
        dates = ohlc.index
        ohlc = ohlc.astype(float)
        ohlc['Dates'] = dates
        plt.style.use('ggplot')
        # Extracting Data for plotting
        ohlc = ohlc.loc[:, ['Dates', 'Open', 'High', 'Low', 'Close', 'Volume']]
        ohlc['Dates'] = pd.to_datetime(ohlc['Dates'])
        ohlc['Dates'] = ohlc['Dates'].apply(mpl_dates.date2num)
        return ohlc

    design_candle = {}

    design_candle['type'] = "candle"
    design_candle['style'] = "charles"
    design_candle['show_notrading'] = False
    design_candle['mav'] = 4
    design_candle['volume'] = True
