import mplfinance as mpf
import matplotlib.animation as animation
from main import Broker
from candles import WorkingFunctions



class Animation:
    tik = input("Choose your destiny: ")
    Broker.dataframe = Broker.form_data(tik)
    dframe = Broker.dataframe
    resample_map = {'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last'}
    resample_period = '1T'

    rs = dframe.resample(resample_period).agg(resample_map).dropna()

    new_candle = rs.iloc[-1]

    def get_new_candle(ticker):
        dframe = Broker.form_data(ticker)

        rs = dframe.resample(Animation.resample_period).agg(Animation.resample_map).dropna()


        if Animation.new_candle[0] != rs.iloc[-1][0] or Animation.new_candle[1] != rs.iloc[-1][1] or Animation.new_candle[2] != rs.iloc[-1][2] or Animation.new_candle[3] != rs.iloc[-1][3]:
            Animation.new_candle = rs.iloc[-1]
            return Animation.new_candle

        else:
            return Animation.get_new_candle(Animation.tik) #!

fig, axes = mpf.plot(Animation.dframe,
                     returnfig=True,
                     type="candle")
ax = axes[0]

# mpf.show()

def animate(ival):

    nxt = Animation.get_new_candle(Animation.tik) #!


    Animation.dframe = Animation.dframe.append(nxt)
    Animation.dframe = Animation.dframe.drop()
    Animation.rs = Animation.dframe.resample(Animation.resample_period).agg(Animation.resample_map).dropna()
    ax.clear()

    last_candle = Animation.rs.iloc[-1]

    mpf.plot(Animation.rs,ax=ax, type="candle")


ani = animation.FuncAnimation(fig, animate, interval=10000)

mpf.show()


