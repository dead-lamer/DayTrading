from data_filler import DataMaker


class Animation:
    dframe = DataMaker.form_data()
    resample_map = {'Open': 'first',
                    'High': 'max',
                    'Low': 'min',
                    'Close': 'last'}
    resample_period = '1T'

    rs = dframe.resample(resample_period).agg(resample_map).dropna()

    new_candle = rs.iloc[-1]

    @classmethod
    def get_new_candle(cls):
        dframe = DataMaker.form_data()

        rs = dframe.resample(Animation.resample_period).agg(Animation.resample_map).dropna()

        if Animation.new_candle[0] != rs.iloc[-1][0] or Animation.new_candle[1] != rs.iloc[-1][1] or Animation.new_candle[2] != rs.iloc[-1][2] or Animation.new_candle[3] != rs.iloc[-1][3]:
            Animation.new_candle = rs.iloc[-1]
            print(Animation.new_candle)
            return Animation.new_candle

        else:
            return Animation.get_new_candle()

