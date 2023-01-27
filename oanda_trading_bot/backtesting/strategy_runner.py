import pandas as pd
import datetime as dt

BUY = 1
SELL = -1
NONE = 0

def apply_take_profit(row):
    if row.trade == NONE:
        return 0.0
    
    if row.SIGNAL == BUY:
        return row.BB_UP
    else:
        return row.BB_LW

def apply_stop_loss(row):
    if row.trade == NONE:
        return 0.0
    
    if row.SIGNAL == BUY:
        return row.mid_l - 0.003
    else:
        return row.mid_h + 0.003

def apply_signals(df: pd.DataFrame, trade_confirmation: function):
    df["SIGNAL"] = df.apply(trade_confirmation, axis=1)
    df["TP"] = df.apply(apply_take_profit, axis=1)
    df["SL"] = df.apply(apply_stop_loss, axis=1)

def create_signals(df, time_d=1):
    df_signals = df[df.SIGNAL != NONE].copy() 

    df_signals['m5_start'] = [x + dt.timedelta(hours=time_d) for x in df_signals.time]

    df_signals.drop(['time', 'mid_o', 'mid_h', 'mid_l', 'bid_o', 'bid_h', 'bid_l',
    'ask_o', 'ask_h', 'ask_l', 'direction'], axis=1, inplace=True)

    df_signals.rename(columns={
        'bid_c' : 'start_price_BUY',
        'ask_c' : 'start_price_SELL',
        'm5_start' : 'time'
    }, inplace=True)

    return df_signals


class StrategyRunner:

    def __init__(self, trade_confirmation: function, df: pd.DataFrame, take_profit: int, stop_loss: int):
        self.df = df.copy()
        self.trade_confirmation = trade_confirmation
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        
        self.prepare_data()
    
    def prepare_data(self):

        apply_signals(self.df, self.take_profit, self.trade_confirmation)

        df = self.df[['time','bid_h', 'bid_l', 'ask_h', 'ask_l' ]].copy()
        df_signals = create_signals(self.df, time_d=self.time_d)

        self.merged = pd.merge(left=df_m5_slim, right=df_signals, on='time', how='left')
        self.merged.fillna(0, inplace=True)
        self.merged.SIGNAL = self.merged.SIGNAL.astype(int)