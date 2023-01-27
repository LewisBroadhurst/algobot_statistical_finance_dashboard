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


class StrategyTester:

    def __init__(self, apply_signal, df, PROFIT_FACTOR, LOSS_FACTOR, use_spread=True):
        self.df = df.copy()
        self.use_spread = use_spread
        self.apply_signal = apply_signal
        self.LOSS_FACTOR = LOSS_FACTOR
        self.PROFIT_FACTOR = PROFIT_FACTOR

        self.prepare_data()
    
    def prepare_data(self):

        apply_signals(self.df_big, self.PROFIT_FACTOR, self.apply_signal)

        df_m5_slim = self.df_m5[['time','bid_h', 'bid_l', 'ask_h', 'ask_l' ]].copy()
        df_signals = create_signals(self.df_big, time_d=self.time_d)

        self.merged = pd.merge(left=df_m5_slim, right=df_signals, on='time', how='left')
        self.merged.fillna(0, inplace=True)
        self.merged.SIGNAL = self.merged.SIGNAL.astype(int)