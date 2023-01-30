import pandas as pd
import datetime as dt
from backtesting.backtesting_models.trade import Trade


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
        self.df_results = pd.merge(left=self.df_results, right=self.df_trades, on=['tp', 'sl', 'trade'])
        return [open_trades, closed_trades]
        