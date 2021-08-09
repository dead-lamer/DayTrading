from data_filler import data_maker
import yfinance as yf


class WorkingFunctions:
    @classmethod
    def find_peak(cls, df=data_maker.form_data()):
        print(df['Open'].max())
        return df['Open'].max()

    @classmethod
    def is_body_long(cls, body):  # [open, close]
        if WorkingFunctions.type_candle(body) == "Bull":  # bull
            if body[1] / body[0] - 1 >= 0.002:
                return True
        elif WorkingFunctions.type_candle(body) == "Bear":  # bear
            if body[0] / body[1] - 1 >= 0.002:
                return True

    @classmethod
    def type_candle(cls, body):
        body[0].to_string()
        body[1].to_string()
        open = body[0]
        close = body[1]
        open = float(open)
        close = float(close)
        if open < close:
            return "Bull"
        if open > close:
            return "Bear"
        else:
            return "Balance"

    last_candle = []

    @classmethod
    def flow_candle(cls, candle):
        if candle is not None:
            open = candle['Open']
            close = candle['Close']
            if len(WorkingFunctions.last_candle) <= 3:
                WorkingFunctions.last_candle.append(WorkingFunctions.type_candle([open, close]))
            else:
                WorkingFunctions.last_candle.remove(WorkingFunctions.last_candle[0])
                WorkingFunctions.last_candle.append(WorkingFunctions.type_candle([open, close]))

        if WorkingFunctions.last_candle == ["Bull", "Bull", "Bull", "Bull"]:
            print("Might be up-trend...")
        if WorkingFunctions.last_candle == ["Bear", "Bear", "Bear", "Bear"]:
            print("Might be down-trend...")
        print(WorkingFunctions.last_candle)


    @classmethod
    def build_candle(cls):
        yf.pdr_override()
        df = data_maker.form_data()
        WorkingFunctions.find_peak(df)
