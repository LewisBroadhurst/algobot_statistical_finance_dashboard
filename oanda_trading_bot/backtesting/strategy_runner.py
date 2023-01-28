import pandas as pd
from backtesting.backtesting_models.trade import Trade

BUY = 1
SELL = -1
NONE = 0


def filter_no_trades_from_df(df):
    df_trades = df[df.trade != NONE].copy() 
    return df_trades


class StrategyRunner:

    def __init__(self, trade_confirmation, df: pd.DataFrame):
        self.df = df.copy()
        self.trade_confirmation = trade_confirmation
        # self.df["trade"] = self.df.apply(trade_confirmation, axis=1)
        self.df = filter_no_trades_from_df(self.df)

    
    def run_test(self):
        open_trades = []
        closed_trades = []

        for _, row in self.df.iterrows():
            if row.trade != NONE:
                open_trades.append(Trade(row))
        
            for ot in open_trades:
                ot.tp_sl_check(row)
                if ot.open == False:
                    closed_trades.append(ot)

        return open_trades