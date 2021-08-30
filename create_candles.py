# for creation of special candles

from datetime import datetime as dt
import pandas as pd


def create_c():
     d = {'Open': [55, 55, 55, 55, ],
          'High': [56, 56, 56, 56, ],
          'Low': [55, 55, 55, 55, ],
          'Close': [56, 56, 56, 56, ],
          'Volume': [100, 999, 98, 97, 96, 995]}
     df = pd.DataFrame(data=d, index=[dt.fromisoformat("2021-08-27 15:55:00-04:00"),
                                      dt.fromisoformat("2021-08-27 15:56:00-04:00"),
                                      dt.fromisoformat("2021-08-27 15:57:00-04:00"),
                                      dt.fromisoformat("2021-08-27 15:58:00-04:00"),
                                      dt.fromisoformat("2021-08-27 15:59:00-04:00"),
                                      dt.fromisoformat("2021-08-28 09:30:00-04:00")])
     return df


create_c()
