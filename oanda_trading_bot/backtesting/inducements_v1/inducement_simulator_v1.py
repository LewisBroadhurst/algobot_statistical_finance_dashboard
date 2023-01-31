import pandas as pd
import datetime as dt


class InducementSimulatorV1:

    def __init__(self, entry_df: pd.DataFrame, trade_confirmation_func, tp_func, sl_func):
        self.df = entry_df.copy()
        self.trade_confirmation_func = trade_confirmation_func
        self.tp_func = tp_func
        self.sl_func = sl_func

        self.df["sTime"] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df.time]
        self.df["trade"] = self.df.apply(trade_confirmation_func, axis=1)
        self.df["tp"] = self.df.apply(tp_func, axis=1)
        self.df["sl"] = self.df.apply(sl_func, axis=1)

    def run_simulation(self):
        pass

