import animative_data
import mplfinance as mpf
import matplotlib.animation as animation

ma = animative_data.MainAnimation()

def get_ticker():
    ticker = input("Choose your destiny: ")
    return ticker


fig, axes = mpf.plot(ma.dframe,
                     returnfig=True,
                     type="candle")
ax = axes[0]

def animate(ival):
    nxt = ma.get_new_candle()  # !
    ma.dframe = ma.dframe.append(nxt)
    ma.rs = ma.dframe.resample(ma.resample_period).agg(ma.resample_map).dropna()
    ax.clear()
    mpf.plot(ma.rs, ax=ax, type="candle")


ani = animation.FuncAnimation(fig, animate, interval=250)

mpf.show()


#TODO сделать модель для тренда цены
#TODO (через верхнюю и нижнюю границу, возможно, с помощью углов наклона "пола" и "потолка")
