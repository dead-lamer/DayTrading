# for creation of special candles

from datetime import datetime as dt
import pandas as pd


def create_c():
     d = {'Open': [52, 50, 55, 59],
          'High': [53, 56, 57, 59],
          'Low': [55, 50, 55, 51],
          'Close': [55, 56, 57, 51]}
     df = pd.DataFrame(data=d, index=[dt.fromisoformat("2020-08-20"),
                                      dt.fromisoformat("2020-08-21"),
                                      dt.fromisoformat("2020-08-22"),
                                      dt.fromisoformat("2020-08-23")])
     return df


create_c()

