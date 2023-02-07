import pandas as pd
import datetime as dt
from charting.indicators import BollingerBands, RSI, ATR
from charting.candle_patterns import apply_candle_props, apply_marubozu
from charting.candle_plot import CandlePlot
import plotly.graph_objects as go


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
        # self.df = BollingerBands(self.df)
        # self.df = RSI(self.df, 10)
        self.df = ATR(self.df, 7)
        self.df["sTime"] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df.time]
        self.df["OB"] = self.df.apply(apply_marubozu, axis=1)

        self.df_merge = None
        self.cp = None
        self.cp_df = None

        self.pdh = 0
        self.pdl = 0
        self.tp = 0
        self.sl = 0
        self.trades_today = 0


    def refresh_hod_lod(self, row, df):
        if row.time.hour == 22 and row.time.minute == 0:
            if (row.name - (288 * 2)) < 0:
                self.pdh = 0

            else:
                if self.pdh != 0 != self.pdl:
                    return
                else:
                    pass

                start_of_pd = row.name - 288
                end_of_pd = row.name

                df_hod = df.iloc[start_of_pd:end_of_pd].copy()
                hod = df_hod.mid_h.max()

                df_lod = df.iloc[start_of_pd:end_of_pd].copy()
                lod = df_lod.mid_h.max()

                self.pdh = hod
                self.pdl = lod




    def max_trade_check(self, row):
        if row.time.hour == 22 and row.time.minute == 0:
            self.trades_today = 0


    def create_sim_candle_plot(self, df):
        self.cp = CandlePlot(df)

        self.cp.fig.add_trace(go.Line(
            x=self.df_merge.sTime,
            y=self.df_merge.tp,
            mode='markers',
            name='tp',
            marker=dict(size=5, color='#00FF00')
        ))
        self.cp.fig.add_trace(go.Line(
            x=self.df_merge.sTime,
            y=self.df_merge.sl,
            mode='markers',
            name='sl',
            marker=dict(size=5, color='#FF0000')
        ))

        self.cp_df = self.cp.df_plot


    def run_simulation(self):
        # TODO: move to BE or close after e.g. 1Hr open
        # TODO: close trades after opening
        open_trades = []
        closed_trades = []

        for _, row in self.df.iterrows():
            self.refresh_hod_lod(row, self.df)
            self.max_trade_check(row)

            if self.trades_today > 2:
                open_trades.append(Trade(0, None, None, None, row.time))

            elif (row.mid_h - 0.00100) > self.pdh != 0 \
                    and row.direction == -1 \
                    and row.OB is True \
                    and 8 < row.time.hour < 12:
                time = row.time
                sl = row.mid_c + 0.0020
                tp = row.mid_c - 0.0060
                entry_price = row.mid_c

                open_trades.append(Trade(1, entry_price, tp, sl, time))
                self.trades_today += 1

            else:
                open_trades.append(Trade(0, None, None, None, row.time))

        df_trades = pd.DataFrame([{'trade': s.trade, 'entry': s.entry_price, 'tp': s.tp, 'sl': s.sl, 'time': s.time}
                                  for s in open_trades])

        self.df_merge = pd.merge(left=self.df, right=df_trades, on=['time'])

        self.create_sim_candle_plot(self.df_merge)

        return self.df_merge
