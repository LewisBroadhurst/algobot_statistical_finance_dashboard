import pandas as pd
import datetime as dt
from charting.indicators import BollingerBands, RSI
from charting.candle_patterns import apply_candle_props, apply_marubozu
from charting.candle_plot import CandlePlot


class Trade:
    def __init__(self, trade, entry_price, tp, sl, time):
        self.trade = trade
        self.entry_price = entry_price
        self.tp = tp
        self.sl = sl
        self.time = time


class InducementSimulatorV1:

    def __init__(self, entry_df: pd.DataFrame):
        self.df = entry_df.copy()
        self.df = apply_candle_props(self.df)
        self.df = BollingerBands(self.df)
        self.df = RSI(self.df, 10)
        self.df["sTime"] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df.time]
        self.df["OB"] = self.df.apply(apply_marubozu, axis=1)
        self.df_merge = None

        self.pdh = 0
        self.pdl = 0
        self.tp = 0
        self.sl = 0

        self.cp = CandlePlot(self.df)
        self.cp.add_ema_traces([5, 20])
        self.cp.add_indicator_traces(["BB_UP"])

        self.df = self.cp.df_plot


    def refresh_hod(self, row, df):
        if row.time.hour == 22 and row.time.minute == 0:
            if row.name - 288 < 0:
                self.pdh = 0

            else:
                start_of_pd = row.name - 288
                end_of_pd = row.name

                df_hl = df.iloc[start_of_pd:end_of_pd].copy()
                hod = df_hl.mid_h.max()

                self.pdh = hod

    def run_simulation(self):
        open_trades = []
        closed_trades = []

        for _, row in self.df.iterrows():
            self.refresh_hod(row, self.df)

            if row.mid_h > self.pdh != 0 and row.direction == -1 and row.OB is True:
                time = row.time
                sl = row.mid_c + 0.0020
                tp = row.mid_c - 0.0060
                entry_price = row.mid_c

                open_trades.append(Trade(1, entry_price, tp, sl, time))

            else:
                open_trades.append(Trade(0, None, None, None, row.time))

        df_trades = pd.DataFrame([{'trade': s.trade, 'entry': s.entry_price, 'tp': s.tp, 'sl': s.sl, 'time': s.time} for s in open_trades])
        self.df_merge = pd.merge(left=self.df, right=df_trades, on=['time'])

        return self.df_merge
