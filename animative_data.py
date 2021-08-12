import data_filler

dm = data_filler.DataMaker()

class MainAnimation:
    dframe = dm.form_data()
    resample_map = {'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last'}
    resample_period = '1T'

    rs = dframe.resample(resample_period).agg(resample_map).dropna()

    new_candle = rs.iloc[-1]

    @classmethod
    def get_new_candle(cls):
        dframe = dm.form_data()

        rs = dframe.resample(MainAnimation.resample_period).agg(MainAnimation.resample_map).dropna()

        if MainAnimation.new_candle[0] != rs.iloc[-1][0] or MainAnimation.new_candle[1] != rs.iloc[-1][1] or MainAnimation.new_candle[2] != rs.iloc[-1][2] or MainAnimation.new_candle[3] != rs.iloc[-1][3]:
            MainAnimation.new_candle = rs.iloc[-1]
            print(MainAnimation.new_candle)
            return MainAnimation.new_candle

        else:
            return MainAnimation.get_new_candle()


