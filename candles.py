from InfromStocks.main import amen

class ReversalPatterns:

    @classmethod
    def find_peak(cls, df): #!
        peak_top1 = df[-5:]['Open'].max()
        peak_top2 = df[-5:]['Close'].max()
        for i in range(len(df)-3, len(df)-1):
            # for the last 5 dframes
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
        peak_low1 = df[-5:]['Open'].min()
        peak_low2 = df[-5:]['Close'].min()
        for i in range(len(df)-3, len(df)-1): # for the last 5 dframes
            if df.iloc[i]['Open'] == peak_low1:
                peak_low1 = df.iloc[i]['Open']
            if df.iloc[i]['Close'] == peak_low2:
                peak_low2 = df.iloc[i]['Close']

            if peak_low1 < peak_low2:
                return peak_low1
            else:
                return peak_low2

    @classmethod
    def is_body_long(cls, rs, body):  # [open, close]
        delta = abs(ReversalPatterns.find_common_candle(rs)['Close'] - ReversalPatterns.find_common_candle(rs)['Open'])
        if abs(body[1] - body[0]) > delta:
            return True
        else:
            return False



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
    def find_common_candle(cls, rs):
        common_open = sum(rs['Open'])/len(rs)
        common_close = sum(rs['Close']) / len(rs)
        common_high = sum(rs['High']) / len(rs)
        common_low = sum(rs['Low']) / len(rs)

        return {"Open" : common_open,
                "Close": common_close,
                "High" : common_high,
                "Low" : common_low}

    @classmethod
    def flow_candle(cls, rs):
        # input : resampled dataframe; checks 2 earlier candles from engulfing pattern
        candle1 = rs.iloc[-3]
        candle2 = rs.iloc[-4]

        body1 = [candle1['Open'], candle1['Close']]
        body2 = [candle2['Open'], candle2['Close']]

        print([ReversalPatterns.type_candle(body1), ReversalPatterns.type_candle(body2)])

        if [ReversalPatterns.type_candle(body1), ReversalPatterns.type_candle(body2)] == ['Bull', 'Bull']:
            print("Bull-trend")
            print("####################################################################")
            return "Bull-trend"
        if [ReversalPatterns.type_candle(body1), ReversalPatterns.type_candle(body2)] == ['Bear', 'Bear']:
            print("Bear-trend")
            print("####################################################################")
            return "Bear-trend"


    @classmethod
    def hammer(cls, df): # is on the bottom (goes after down-trend); lower shadow >= real body*2; upper shadow should be gone or tiny,
        to_check = df.iloc[-2]
        candle2 = df.iloc[-1]
        bottom_line = ReversalPatterns.find_bottom(df)

        if ReversalPatterns.type_candle([to_check['Open'], to_check['Close']]) == 'Bull':
            if to_check['Open'] <= bottom_line: #bull
                if to_check['Open'] - to_check['Low'] >= 2*(to_check['Close'] - to_check['Open']):
                    if to_check['High'] - to_check['Close'] <= 0.1*(to_check['Open'] - to_check['Low']):
                        print('Hammer (strong up mood)')
                        print(to_check)
                        print("####################################################################")
                        return amen("Hammer (strong up mood)", to_check)
            else:
                return None

        if ReversalPatterns.type_candle([to_check['Open'], to_check['Close']]) == 'Bear':
            if to_check['Close'] <= bottom_line: #bear
                if to_check['Close'] - to_check['Low'] >= 2*(to_check['Open'] - to_check['Close']):
                    if to_check['High'] - to_check['Open'] <= 0.1*(to_check['Close'] - to_check['Low']):
                        print("Hammer")
                        print(to_check)
                        print("####################################################################")
                        return amen("Hammer", to_check)
            else:
                return None

    @classmethod
    def hanging_man(cls, df): # on the top of price; lower shadow >= real body*2; upper shadow should be gone or tiny
        to_check = df.iloc[-2]
        candle1 = df.iloc[-1]
        top_line = ReversalPatterns.find_peak(df)
        #TODO: if next day starts from point that is lower than hanging man body, it is strong bear-signal (the more is gap between next day point and hanging man the more it (hanging man) is peak)

        if ReversalPatterns.type_candle([to_check['Open'], to_check['Close']]) == 'Bull':
            if to_check['Close'] >= top_line: # bull
                if to_check['Open'] - to_check['Low'] >= 2 * (to_check['Close'] - to_check['Open']):
                    if to_check['High'] - to_check['Close'] <= 0.1*(to_check['Open'] - to_check['Low']):
                    # writing hanging man body
                        if to_check['Open'] > candle1['Open']:
                            print("Hanging man (strong down mood)")
                            print(to_check)
                            print("####################################################################")
                            return amen("Hanging man (strong down mood)", to_check)
                        else:
                            print("Hanging man")
                            print(to_check)
                            print("####################################################################")
                            return amen("Hanging man", to_check)

            else:
                return None

        if ReversalPatterns.type_candle([to_check['Open'], to_check['Close']]) == 'Bear':
            if to_check['Open'] >= top_line: # bear
                if to_check['Close'] - to_check['Low'] >= 2*(to_check['Open'] - to_check['Close']):
                    if to_check['High'] - to_check['Open'] <= 0.1*(to_check['Close'] - to_check['Low']):
                    # writing hanging man body
                        if to_check['Close'] > candle1['Open']:
                            print("Hanging man (strong down mood)")
                            print(to_check)
                            print("####################################################################")
                            return amen("Hanging man (strong down mood)", to_check)
                        else:
                            print("Hanging man (strong down mood)")
                            print(to_check)
                            print("####################################################################")
                            return amen("Hanging man (strong down mood)", to_check)
            else:
                return None


    @classmethod
    def engulfing_pattern(cls, df):
        # rs input only
        trend = ReversalPatterns.flow_candle(df)
        candle2 = df.iloc[-2]
        # counts from start of plot!!!
        candle1 = df.iloc[-1]


        if trend == 'Bear-trend':
            if (ReversalPatterns.type_candle([candle2['Open'], candle2['Close']]) == 'Bear' or ReversalPatterns.type_candle([candle2['Open'], candle2['Close']]) == 'Doji') and ReversalPatterns.type_candle([candle1['Open'], candle1['Close']]) == 'Bull': # Bull engulfing pattern1
                if candle2['Open'] - candle2['Close'] < candle1['Close'] - candle1['Open']:
                    if candle2['Close'] >= candle1['Open'] and candle2['Open'] <= candle1['Close']:
                        candle3 = df.iloc[-3]
                        if ReversalPatterns.type_candle([candle3['Open'], candle3['Close']]) == "Bear":
                            # strong engulfing signal
                            if (candle3['Open'] - candle3['Close']) + (candle2['Open'] - candle2['Close']) < candle1['Close'] - candle1['Open']:
                                print("Strong Bull Engulfing Pattern (strong up-trend)")
                                print(candle1)
                                return amen("Strong Bull Engulfing Pattern", candle1)
                            else: # usual signal
                                print("Bull Engulfing Pattern (up-trend)")
                                print(candle1)
                                print("####################################################################")
                                return amen('Bull Engulfing Pattern', candle1)

        if trend == 'Bull-trend':
            if (ReversalPatterns.type_candle([candle2['Open'], candle2['Close']]) == 'Bull' or ReversalPatterns.type_candle([candle2['Open'], candle2['Close']]) == 'Doji') and ReversalPatterns.type_candle([candle1['Open'], candle1['Close']]) == 'Bear': # Bear engulfing pattern
                if candle2['Close'] - candle2['Open'] < candle1['Open'] - candle1['Close']:
                    if candle2['Open'] >= candle1['Close'] and candle2['Close'] <= candle1['Open']:
                        candle3 = df.iloc[-3]
                        if ReversalPatterns.type_candle([candle3['Open'], candle3['Close']]) == "Bull":
                            # strong engulfing signal
                            if (candle3['Close'] - candle3['Open']) + (candle2['Close'] - candle2['Open']) < candle1['Open'] - candle1['Close']:
                                print("Strong Bear Engulfing Pattern (strong down-trend)")
                                print(candle1)
                                return amen("Strong Bear Engulfing Pattern", candle1)
                            else: # usual signal
                                print("Bear Engulfing Pattern (down-trend)")
                                print(candle1)
                                print("####################################################################")
                                return amen("Bear Engulfing Pattern", candle1)

        else:
            return None


    @classmethod
    def dark_cloud_cover(cls, df):
        trend = ReversalPatterns.flow_candle(df)
        # is counted from left
        candle2 = df.iloc[-2]
        candle1 = df.iloc[-1]
        if trend == "Bull-trend":
            if ReversalPatterns.is_body_long(df, [candle1['Open'], candle1['Close']]) and ReversalPatterns.is_body_long(df, [candle2['Open'], candle2['Close']]):
                if ReversalPatterns.type_candle([candle2['Open'], candle2['Close']]) == 'Bull' and ReversalPatterns.type_candle([candle1['Open'], candle1['Close']]) == 'Bear':
                    if candle2['High'] <= candle1['Open'] and candle2['Open'] < candle1['Close']:
                        if candle1['Open'] == ReversalPatterns.find_peak(df): # strong signals
                            print("Strong Dark Cloud Cover (strong down-trend)")
                            print(candle1)
                            print("####################################################################")
                            return amen("Strong Dark Cloud Cover", candle1)
                        elif candle2['High'] == candle2['Close'] and candle2['Low'] == candle2['Open'] and candle1['High'] == candle1['Open'] and candle1['Low'] == candle1['Close']:
                            print("Strong Dark Cloud Cover (strong down-trend)")
                            print(candle1)
                            print("####################################################################")
                            return amen("Strong Dark Cloud Cover", candle1)
                        elif (candle2['Close'] - candle2['Open'])/2.0 + candle2['Open'] < candle1['Open']:
                            print("Strong Dark Cloud Cover (strong down-trend)")
                            print(candle1)
                            print("####################################################################")
                            return amen("Strong Dark Cloud Cover", candle1)
                        else: # usual signals
                            print("Dark cloud cover (down-trend)")
                            print(candle1)
                            print("####################################################################")
                            return amen("Dark Cloud Cover", candle1)
        else:
            return None


    @classmethod
    def piercing_pattern(cls, df):
        trend = ReversalPatterns.flow_candle(df)
        # is counted from left
        candle2 = df.iloc[-2]
        candle1 = df.iloc[-1]
        if trend == "Bear-trend":
            if ReversalPatterns.is_body_long(df, [candle1['Open'], candle1['Close']]) and ReversalPatterns.is_body_long(df, [candle2['Open'], candle2['Close']]):
                if ReversalPatterns.type_candle([candle2['Open'], candle2['Close']]) == "Bear" and ReversalPatterns.type_candle([candle1['Open'], candle1['Close']]) == "Bull":
                    if (candle2['Open'] - candle2['Close'])/2.0 + candle2['Close'] < candle1['Close'] and candle2['Low'] > candle1['Open'] and candle2['Open'] > candle1['Close']:
                        if candle1['High'] == candle1['Close'] and candle1['Low'] == candle1['Open']:
                            print("Strong Piercing Pattern (strong up-trend)")
                            print(candle1)
                            print("####################################################################")
                            return amen("Strong Piercing Pattern", candle1)
                        else:
                            print("Piercing Pattern (up-trend)")
                            print(candle1)
                            print("####################################################################")
                            return amen("Piercing Pattern", candle1)
        else:
            return None


    @classmethod
    def on_neck(cls, df):
        trend = ReversalPatterns.flow_candle(df)
        # is counted from left
        candle2 = df.iloc[-3]
        candle1 = df.iloc[-2]
        if trend == "Bear-trend":
            if ReversalPatterns.type_candle([candle2['Open'], candle2['Close']]) == "Bear" and ReversalPatterns.type_candle([candle1['Open'], candle1['Close']]) == "Bull":
                if candle2['Low'] <= candle1['Close'] and candle2['Close'] > candle1['Close']:
                    candle3 = df.iloc[-1]
                    if candle3['High'] < candle1['Low']:
                        print("Strong on-neck (strong down trend)")
                        print(candle1)
                        print("####################################################################")
                        return amen("Strong on-neck", candle1)

                    else:
                        print("On-neck (down-trend)")
                        print(candle1)
                        print("####################################################################")
                        return amen("On-neck", candle1)
        else:
            return None




    @classmethod
    def in_neck(cls, df):
        trend = ReversalPatterns.flow_candle(df)
        # is counted from left
        candle2 = df.iloc[-3]
        candle1 = df.iloc[-2]
        if trend == "Bear-trend":
            if ReversalPatterns.type_candle([candle2['Open'], candle2['Close']]) == "Bear" and ReversalPatterns.type_candle([candle1['Open'], candle1['Close']]) == "Bull":
                if candle2['Close'] <= candle1['Close'] and candle1['Close'] <= (candle2['Open'] - candle2['Close'])/4 + candle2['Close']:
                    candle3 = df.iloc[-1]
                    if candle3['High'] < candle1['Low']:
                        print("Strong in-neck (strong down trend)")
                        print(candle1)
                        print("####################################################################")
                        return amen("Strong in-neck", candle1)
                    else:
                        print("In-neck (down-trend)")
                        print(candle1)
                        print("####################################################################")
                        return amen("In-neck", candle1)
        else:
            return None

    @classmethod
    def thrusting_pattern(cls):
        pass


class Stars:
    pass

