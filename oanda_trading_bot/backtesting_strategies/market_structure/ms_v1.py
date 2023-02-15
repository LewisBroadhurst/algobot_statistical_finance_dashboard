import pandas as pd
from backtesting_strategies.concepts.market_structure import MarketStructure
from charting.price_time_chart import PriceTimeChart


class MS1:

    def __init__(self, m5_df: pd.DataFrame):
        self.df = m5_df.copy()
        self.trades = 0
        self.marketStructure = MarketStructure(m5_df)

        self.cp = PriceTimeChart(m5_df, "line")
        self.cp_df = self.cp.df_plot
        self.cp_df.row["trade"] = 0
        self.cp_df.row["sl"] = 0
        self.cp_df.row["tp"] = 0

    def run_backtest(self):
        open_trades = []
        closed_trades = []

        for index, row in self.df.iterrows():
            x = self.marketStructure.run_uptrend_downtrend_func(row)

            if x is None:
                self.df["trade"] = 0
                self.df["sl"] = 0
                self.df["tp"] = 0
                print("NONE")
            else:
                if x[0] == 1:
                    print("open trade", x)
                    self.df["trade"] = 1
                    self.df["sl"] = x[1]
                    self.df["tp"] = x[2]

                elif x[0] == -1:
                    print("open trade", x)
                    self.df["trade"] = -1
                    self.df["sl"] = x[1]
                    self.df["tp"] = x[2]

        return self.df
