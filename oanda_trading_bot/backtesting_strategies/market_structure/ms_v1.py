import pandas as pd
from backtesting_strategies.concepts.market_structure import MarketStructure
from charting.price_time_chart import PriceTimeChart
from models.trade import Trade


class MS1:

    def __init__(self, m5_df: pd.DataFrame, start_bullish_or_bearish: str):
        self.df = m5_df.copy()
        self.start_bullish_or_bearish = start_bullish_or_bearish

        self.df['trade'] = 0
        self.df['sl'] = 0
        self.df['tp'] = 0

        self.marketStructure = MarketStructure(m5_df, start_bullish_or_bearish)
        self.cp = PriceTimeChart(m5_df, "line")

    def prepare_data(self):

        for index, row in self.df.iterrows():
            x = self.marketStructure.run_uptrend_downtrend_func(row)

            if x is not None:
                if x[0] == 1 and x[1] != 0 != x[2]:
                    self.df.at[index, 'trade'] = x[0]
                    self.df.at[index, 'sl'] = x[1]
                    self.df.at[index, 'tp'] = x[2]

                elif x[0] == -1 and x[1] != 0 != x[2]:
                    print("open trade", x)
                    self.df.at[index, 'trade'] = x[0]
                    self.df.at[index, 'sl'] = x[1]
                    self.df.at[index, 'tp'] = x[2]

                else:
                    self.df.at[index, 'trade'] = 0
                    self.df.at[index, 'sl'] = 0
                    self.df.at[index, 'tp'] = 0

            else:
                self.df.at[index, 'trade'] = 0
                self.df.at[index, 'sl'] = 0
                self.df.at[index, 'tp'] = 0

        return self.df
