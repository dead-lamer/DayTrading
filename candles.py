class WorkingFunctions:
    @classmethod
    def find_peak(cls, df):
        peak_top1 = df[-8:]['Open'].max()
        peak_top2 = df[-8:]['Close'].max()
        for i in range(len(df)-8, len(df)-1): # for the last 7 dframes
            if df.iloc[i]['Open'] == peak_top1:
                peak_top1 = df.iloc[i]['Open']
            if df.iloc[i]['Close'] == peak_top2:
                peak_top2 = df.iloc[i]['Close']

            if peak_top1 > peak_top2:
                return peak_top1
            else:
                return peak_top2


    @classmethod
    def find_bottom(cls, df):
        peak_low1 = df[-8:]['Open'].min()
        peak_low2 = df[-8:]['Close'].min()
        for i in range(len(df)-8, len(df)-1): # for the last 7 dframes
            if df.iloc[i]['Open'] == peak_low1:
                peak_low1 = df.iloc[i]['Open']
            if df.iloc[i]['Close'] == peak_low2:
                peak_low2 = df.iloc[i]['Close']

            if peak_low1 < peak_low2:
                return peak_low1
            else:
                return peak_low2

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
        open_ = body[0]
        close = body[1]
        if open_ is None and close is None:
            print("No candle")
            return None
        else:
            if open_ < close:
                return "Bull"
            if open_ > close:
                return "Bear"
            if open_ == close:
                return "Doji"

    last_candle = []


    @classmethod
    def flow_candle(cls, rs): # input : resampled dataframe; checks 2 earlier candles from engulfing pattern
        candle1 = rs.iloc[-3]
        candle2 = rs.iloc[-4]

        body1 = [candle1['Open'], candle1['Close']]
        body2 = [candle2['Open'], candle2['Close']]


        if [WorkingFunctions.type_candle(body1), WorkingFunctions.type_candle(body2)] == ['Bull' 'Bull']:
            print("Bull-trend")
            print("#########################################################################")
            return "Bull-trend"
        if [WorkingFunctions.type_candle(body1), WorkingFunctions.type_candle(body2)] == ['Bear', 'Bear']:
            print("Bear-trend")
            print("#########################################################################")
            return "Bear-trend"


    @classmethod
    def hammer(cls, df): # is on the bottom (goes after down-trend); lower shadow >= real body*2; upper shadow should be gone or tiny,
        to_check = df.iloc[-2]
        bottom_line = WorkingFunctions.find_bottom(df)


        if to_check['Open'] <= bottom_line: #bull
            if to_check['Open'] - to_check['Low'] >= 2*(to_check['Close'] - to_check['Open']):
                if to_check['Close'] == to_check['High'] or to_check:
                    print('Hammer')
                    print(to_check)
                    print("#########################################################################")
                    return "Hammer"


        if to_check['Close'] <= bottom_line: #bear
            if to_check['Close'] - to_check['Low'] >= 2*(to_check['Open'] - to_check['Close']):
                if to_check['Open'] == to_check['High']:
                    print("Hammer")
                    print(to_check)
                    print("#########################################################################")
                    return "Hammer"

    @classmethod
    def hanging_man(cls, df): # on the top of price; lower shadow >= real body*2; upper shadow should be gone or tiny
        to_check = df.iloc[-2]
        top_line = WorkingFunctions.find_peak(df)


        if to_check['Close'] >= top_line: # bull
            if to_check['Open'] - to_check['Low'] >= 2 * (to_check['Close'] - to_check['Open']):
                if to_check['Close'] == to_check['High']:
                    print("Hanging man")
                    print(to_check)
                    print("#########################################################################")
                    return "Hanging man"


        if to_check['Open'] >= top_line: # bear
            if to_check['Close'] - to_check['Low'] >= 2*(to_check['Open'] - to_check['Close']):
                if to_check['Open'] == to_check['High']:
                    print("Hanging man")
                    print(to_check)
                    print("#########################################################################")
                    return "Hanging man"


    @classmethod
    def engulfing_pattern(cls, df):
        trend = WorkingFunctions.flow_candle(df)
        candle1 = df.iloc[-2]
        candle2 = df.iloc[-1]

        if trend == 'Bear-trend':
            if WorkingFunctions.type_candle([candle1['Open'], candle1['Close']]) == 'Bear' and WorkingFunctions.type_candle([candle2['Open'], candle2['Close']]) == 'Bull': # Bull engulfing pattern
                if candle1['Open'] - candle1['Close'] < candle2['Close'] - candle2['Open']:
                    print("Bull Engulfing Pattern")
                    print(candle2)
                    print("#########################################################################")
                    return 'Bull Engulfing Pattern'

        if trend == 'Bull-trend':
            if WorkingFunctions.type_candle([candle1['Open'], candle1['Close']]) == 'Bull' and WorkingFunctions.type_candle([candle2['Open'], candle2['Close']]) == 'Bear': # Bear engulfing pattern
                if candle1['Close'] - candle1['Open'] < candle2['Open'] - candle2['Close']:
                    print("Bear Engulfing Pattern")
                    print(candle2)
                    print("#########################################################################")
                    return "Bear Engulfing Pattern"

        else:
            return None



