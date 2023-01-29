import pandas as pd
import datetime as dt
from backtesting.backtesting_models.trade import Trade

def trade_confirmation_func(row):
    if row.ask_c < row.BB_LW:
        return 1
    if row.bid_c > row.BB_UP:
        return -1
    return 0
    
def tp_func(row):
    if row.trade == 1:
        return row.ask_c * 1.005
    if row.trade == -1:
        return row.bid_c * 1.005

def sl_func(row):
    if row.trade == 1:
        return row.ask_c * 0.995
    if row.trade == -1:
        return row.bid_c * 0.995

class BbAsrV1:

    def __init__(self, entry_df: pd.DataFrame, trade_confirmation_func, tp_func, sl_func):
        self.df = entry_df.copy()
        self.trade_confirmation_func = trade_confirmation_func
        self.tp_func = tp_func
        self.sl_func = sl_func

        self.df["sTime"] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df.time]
        self.df["trade"] = self.df.apply(trade_confirmation_func, axis=1)
        self.df = self.df[self.df.trade != 0].copy()
        self.df["tp"] = self.df.apply(tp_func, axis=1)
        self.df["sl"] = self.df.apply(sl_func, axis=1)

        self.df_trades = self.df.copy()
        self.df_trades = self.df_trades[self.df_trades.trade != 0].copy()
        self.df_trades.reset_index(drop=True, inplace=True)
    

    def run_simulation(self):
        open_trades = []
        closed_trades = []

        for _, row in self.df_trades.iterrows():
            if row.trade != 0:
                open_trades.append(Trade(row, self.tp_func, self.sl_func))
        
            for ot in open_trades:
                ot.tp_sl_check(row)

                if ot.open == False:
                    closed_trades.append(ot)
        
        self.df_results = pd.DataFrame.from_dict([vars(x) for x in closed_trades])
        return [open_trades, closed_trades]
        