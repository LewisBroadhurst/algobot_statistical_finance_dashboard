import pandas as pd
from backtesting_strategies.concepts.market_structure import MarketStructure
from charting.price_time_chart import PriceTimeChart


class MS1:

    def __init__(self, m5_df: pd.DataFrame):
        self.df = m5_df.copy()
        self.trades = 0
        self.marketStructure = MarketStructure(m5_df)
        self.cp = PriceTimeChart(m5_df, "line")

    def run_backtest(self):
        open_trades = []
        closed_trades = []

        for _, row in self.df.iterrows():
            x = self.marketStructure.run_uptrend_downtrend_func(row)

            if x is not None:

                if x[0] == 1:
                    print("open trade", x)
                    self.cp.df_plot["trade"] = 1
                    self.cp.df_plot["sl"] = x[1]
                    self.cp.df_plot["tp"] = x[2]

                elif x[0] == -1:
                    print("open trade", x)
                    self.cp.df_plot["trade"] = -1
                    self.cp.df_plot["sl"] = x[1]
                    self.cp.df_plot["tp"] = x[2]

                else:
                    self.cp.df_plot["trade"] = 0
                    self.cp.df_plot["sl"] = 0
                    self.cp.df_plot["tp"] = 0
