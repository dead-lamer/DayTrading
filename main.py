from animation import Animation
import mplfinance as mpf
import matplotlib.animation as animation


def get_ticker():
    ticker = input("Choose your destiny: ")
    return ticker


fig, axes = mpf.plot(Animation.dframe,
                     returnfig=True,
                     type="candle")
ax = axes[0]


def animate(ival):
    nxt = Animation.get_new_candle()  # !
    Animation.dframe = Animation.dframe.append(nxt)
    Animation.rs = Animation.dframe.resample(Animation.resample_period).agg(Animation.resample_map).dropna()
    ax.clear()
    mpf.plot(Animation.rs, ax=ax, type="candle")


ani = animation.FuncAnimation(fig, animate, interval=250)

mpf.show()


#TODO сделать модель для тренда цены
#TODO (через верхнюю и нижнюю границу, возможно, с помощью углов наклона "пола" и "потолка")
