import mplfinance as mpf
import matplotlib.animation as animation

# import create_candles

from main import Broker
from candles import WorkingFunctions


class Animation:
    tik = input("Choose your destiny: ")
    Broker.dataframe = Broker.form_data(tik)
    dframe = Broker.dataframe

    # dframe = create_candles.create_c()

    last_time_index = dframe.index[-1]

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
                     type="candle",
                     style=Broker.design_candle['style'],
                     mav=Broker.design_candle['mav'])
ax = axes[0]

# WorkingFunctions.engulfing_pattern(Animation.rs)
# WorkingFunctions.dark_cloud_cover(Animation.rs)
# WorkingFunctions.piercing_pattern(Animation.rs)

# mpf.show()

def animate(ival):
    nxt = Animation.get_new_candle(Animation.tik)

    Animation.dframe = Animation.dframe.append(nxt)

    ax.clear()

    if Animation.dframe.index[-1] != Animation.last_time_index:
        Animation.dframe = Animation.dframe.drop([Animation.dframe.index[0]])

    Animation.rs = Animation.dframe.resample(Animation.resample_period).agg(Animation.resample_map).dropna()  #

    Animation.last_time_index = Animation.dframe.index[-1]

    WorkingFunctions.hammer(Animation.rs)
    WorkingFunctions.hanging_man(Animation.rs)
    WorkingFunctions.engulfing_pattern(Animation.rs)
    WorkingFunctions.dark_cloud_cover(Animation.rs)
    WorkingFunctions.piercing_pattern(Animation.rs)

    mpf.plot(Animation.rs, ax=ax,
            type="candle",
            style=Broker.design_candle['style'],
            mav=Broker.design_candle['mav']
            )


ani = animation.FuncAnimation(fig, animate, interval=10000)

mpf.show()

# this could help to add volume plot:
# import pandas as pd
# import mplfinance as mpf
# ohlcv = pd.DataFrame(
#    {'Date': [1609459200, 1609545600, 1609632000, 1609718400,
#              1609804800, 1609891200, 1609977600, 1610064000],
#     'Open': [11.25, 12.61, 11.93, 10.52, 10.41, 11.66, 11.47, 12.14],
#     'High': [12.63, 13.2, 11.94, 12.12, 15.02, 11.71, 12.47, 13.01],
#     'Low': [11.10, 11.68, 9.93, 10.3, 10.31, 11.26, 10.46, 12.13],
#     'Close': [12.61, 11.93, 10.52, 10.41, 11.66, 11.47, 12.14, 12.96],
#     'Volume': [108, 102, 105, 116, 164, 145, 132, 117],
#     'cash': [100.0, 100.295, 100.295, 100.295, 95.685, 95.635, 95.635, 95.635]
#     })
#
#ohlcv.iloc[:, 0] = pd.to_datetime(ohlcv.iloc[:, 0], unit='s')
#ohlcv = ohlcv.set_index('Date')
#
#ap = mpf.make_addplot(ohlcv['cash'],panel=0,ylabel='Cash')
#mpf.plot(ohlcv,
#         type='candle',
#         volume=True,
#         main_panel=1,
#         volume_panel=2,
#         addplot=ap,
#         figsize=(7,7))