import pandas as pd

class InducementsV1Runner:

    def __init__(self, df: pd.DataFrame, trade_confirmation):
        self.df = df.copy()
        self.df_slim = self.df[['time', 'bid_h', 'bid_l', 'ask_h', 'ask_l']].copy()


