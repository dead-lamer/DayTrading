from animative_data import main_animation
import mplfinance as mpf
import matplotlib.animation as animation


def get_ticker():
    ticker = input("Choose your destiny: ")
    return ticker


fig, axes = mpf.plot(main_animation.dframe,
                     returnfig=True,
                     type="candle")
ax = axes[0]


def animate(ival):
    nxt = main_animation.get_new_candle()  # !
    main_animation.dframe = main_animation.dframe.append(nxt)
    main_animation.rs = main_animation.dframe.resample(main_animation.resample_period).agg(main_animation.resample_map).dropna()
    ax.clear()
    mpf.plot(main_animation.rs, ax=ax, type="candle")


ani = animation.FuncAnimation(fig, animate, interval=250)

mpf.show()


#TODO сделать модель для тренда цены
#TODO (через верхнюю и нижнюю границу, возможно, с помощью углов наклона "пола" и "потолка")
