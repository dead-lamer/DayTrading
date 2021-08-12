class WorkingFunctions:
    @classmethod
    def find_peak(cls, df):
        peak_open = df['Open'].max()
        for i in range(0, len(df)-1):
            if df.iloc[i]['Open'] == peak_open:
                print(df.iloc[i])
                return df.iloc[i]

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
        open = body[0]
        close = body[1]
        if open < close:
            print("Bull")
            return "Bull"
        if open > close:
            print("Bear")
            return "Bear"
        else:
            print("Doji")
            return "Doji"

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
    def hammer(cls): # is on the bottom; lower shadow >= real body*2; upper shadow should be gone or tiny
        pass

    @classmethod
    def hanging_man(cls, df): # on the top of price; lower shadow >= real body*2; upper shadow should be gone or tiny
        to_check = WorkingFunctions.find_peak(df) # open: 55:54 max: 55:55
        if (to_check['Close'] - to_check['Low'] >= 2*(to_check['Open'] - to_check['Close'])) or (to_check['Open'] - to_check['Low'] >= 2*(to_check['Close'] - to_check['Open'])):
            if to_check['Open'] == to_check['High'] or to_check['Close'] == to_check['High']:
                type = WorkingFunctions.type_candle([to_check['Open'], to_check['Close']])
                print("Hanging man")
                print(type)


