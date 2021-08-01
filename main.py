from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import matplotlib.dates as mpl_dates
import matplotlib.animation as animation


d = datetime.today().day
m = datetime.today().month
y = datetime.today().year

start = datetime(y-1, m, d)
end = datetime(y, m, d)


class Broker:
    @staticmethod
    def form_data(tik):
        ohlc = pdr.get_data_yahoo(tickers=tik,
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

    @classmethod
    def find_peak(cls, df):
        print(df['Open'].max())
        return df['Open'].max()

    @classmethod
    def is_body_long(cls, body):  # [open, close]
        if Broker.type_candle(body) == "Bull":  # bull
            if body[1] / body[0] - 1 >= 0.002:
                return True
        elif Broker.type_candle(body) == "Bear":  # bear
            if body[0] / body[1] - 1 >= 0.002:
                return True

    @classmethod
    def type_candle(cls, body):
        body[0].to_string()
        body[1].to_string()
        open = body[0]
        close = body[1]
        open = float(open)
        close = float(close)
        if open < close:
            return "Bull"
        if open > close:
            return "Bear"
        else:
            return "Balance"

    last_candle = []

    @classmethod
    def flow_candle(cls, candle):
        if candle is not None:
            open = candle['Open']
            close = candle['Close']
            if len(Broker.last_candle) <= 3:
                Broker.last_candle.append(Broker.type_candle([open, close]))
            else:
                Broker.last_candle.remove(Broker.last_candle[0])
                Broker.last_candle.append(Broker.type_candle([open, close]))

        if Broker.last_candle == ["Bull", "Bull", "Bull", "Bull"]:
            print("Might be up-trend...")
        if Broker.last_candle == ["Bear", "Bear", "Bear", "Bear"]:
            print("Might be down-trend...")
        print(Broker.last_candle)



    design_candle = {}

    design_candle['type'] = "candle"
    design_candle['style'] = "charles"
    design_candle['show_notrading'] = False
    design_candle['mav'] = 4
    design_candle['volume'] = True

    @classmethod
    def build_candle(cls, tik):
        yf.pdr_override()
        #app.get_news(tik)
        df = Broker.form_data(tik)
        Broker.find_peak(df)



        # Creating Subplots
        #mpf.plot(df,
                 #type=Broker.design_candle['type'],
                 #mav=Broker.design_candle['mav'],
                 #style=Broker.design_candle['style'],
                 #show_nontrading=Broker.design_candle["show_notrading"],
                 #title=f"${tik}",
                 #volume=Broker.design_candle['volume'])

        # Setting labels & titles
        # Formatting Date

    @staticmethod
    def get_news(tik):
        import requests
        url = "https://stock-market-data.p.rapidapi.com/stock/buzz/news"
        querystring = {"ticker_symbol":f"{tik}","date":f"{y}-{m}-{d}"}
        headers = {
            'x-rapidapi-key': "11d8bc37d8mshf186de22a127423p1552c3jsnd379e8ad19aa",
            'x-rapidapi-host': "stock-market-data.p.rapidapi.com"
            }
        response = requests.request("GET",
                                    url,
                                    headers=headers,
                                    params=querystring)
        response = response.json()
        news = response['news']
        for i in news:
            for j in i.keys():
                if j == "title":
                    print(i['title'] + "\n")






app = Broker
tik = input("Choose your destiny: ")
app.build_candle(tik)





class RealTimeAPI():
    def __init__(self):
        self.data_pointer = 0
        self.data_frame = Broker.form_data(tik)
        #self.data_frame = self.data_frame.iloc[0:120,:]
        self.df_len = len(self.data_frame)

    def fetch_next(self):
        r1 = self.data_pointer
        self.data_pointer += 1
        if self.data_pointer >= self.df_len:
            return None
        return self.data_frame.iloc[r1:self.data_pointer,:]

    def initial_fetch(self):
        if self.data_pointer > 0:
            return
        r1 = self.data_pointer
        self.data_pointer += int(0.2*self.df_len)
        return self.data_frame.iloc[r1:self.data_pointer,:]

rtapi = RealTimeAPI()

resample_map ={'Open': 'first',
               'High': 'max',
               'Low': 'min',
               'Close': 'last'}
resample_period = '1min'

df = rtapi.initial_fetch()
rs = df.resample(resample_period).agg(resample_map).dropna()

fig, axes = mpf.plot(rs,
                     returnfig=True,
                     figsize=(11,8),
                     type=Broker.design_candle['type'],
                     title=f'${tik}',
                     style=Broker.design_candle['style'],
                     show_nontrading=Broker.design_candle['show_notrading'],
                     mav=Broker.design_candle['mav'])
ax = axes[0]

def animate(ival):
    global df
    global rs
    nxt = rtapi.fetch_next()
    Broker.flow_candle(nxt)
    if nxt is None:
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            pass
            #exit()
        return
    df = df.append(nxt)
    rs = df.resample(resample_period).agg(resample_map).dropna()
    ax.clear()
    mpf.plot(rs,
             ax=ax,
             type=Broker.design_candle['type'],
             style=Broker.design_candle['style'],
             mav=Broker.design_candle['mav']
             )

ani = animation.FuncAnimation(fig, animate, interval=250)

mpf.show()





##TODO сделать модель для тренда цены
##TODO (через верхнюю и нижнюю границу, возможно, с помощью углов наклона "пола" и "потолка")
