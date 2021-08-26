# for creation of special candles

from datetime import datetime as dt
import pandas as pd


def create_c():
     d = {'Open': [52, 52, 52, 50, 58, 55],
          'High': [53, 53, 53, 56, 58.000464, 57],
          'Low': [55, 55, 55, 50, 51, 55],
          'Close': [55, 55, 55, 56, 57, 57]}
     df = pd.DataFrame(data=d, index=[dt.fromisoformat("2020-08-20"),
                                      dt.fromisoformat("2020-08-21"),
                                      dt.fromisoformat("2020-08-22"),
                                      dt.fromisoformat("2020-08-23"),
                                      dt.fromisoformat("2020-08-24"),
                                      dt.fromisoformat("2020-08-25")])
     return df


create_c()

