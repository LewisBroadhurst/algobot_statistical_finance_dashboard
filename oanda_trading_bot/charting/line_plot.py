import datetime as dt
import plotly.graph_objects as go
import pandas as pd


class LinePlot:

    def __init__(self, df: pd.DataFrame):
        self.df_plot = df.copy()
        self.fig = go.Figure()
        self.create_line_plot()

    def add_timestr(self):
        """Hack for removing weekend candles"""
        self.df_plot['sTime'] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df_plot.time]
    
    def create_line_plot(self):
        self.add_timestr()
        self.fig.add_trace(go.Line(
            x=self.df_plot.sTime,
            y=self.df_plot.mid_c,
            mode='lines',
            name='price'
        ))
    
    def create_rsi(self, df: pd.DataFrame, n=14):
        alpha = 1.0 / n
        gains = self.df_plot.mid_c.diff()

        wins = pd.Series([ x if x >= 0 else 0.0 for x in gains ], name="wins")
        losses = pd.Series([ x * -1 if x < 0 else 0.0 for x in gains ], name="losses")

        wins_rma = wins.ewm(min_periods=n, alpha=alpha).mean()
        losses_rma = losses.ewm(min_periods=n, alpha=alpha).mean()

        rs = wins_rma / losses_rma
        df[f"RSI_{n}"] = 100.0 - (100.0 / (1.0 + rs))

        self.add_timestr()
        self.fig.add_trace(go.Line(
            x=self.df_plot.sTime,
            y=self.df_plot[f"RSI_{n}"],
            mode='lines',
            name=f"RSI_{n}"
        ))
        

    def add_ema_traces(self, ema_list: list):
        for ema in ema_list:
            self.df_plot[f'ema_{ema}'] = self.df_plot.mid_c.ewm(span=ema, min_periods=ema).mean()
            
            self.fig.add_trace(go.Line(
                x=self.df_plot.sTime,
                y=self.df_plot[f"ema_{ema}"],
                mode='lines',
                name=f'{ema} EMA'
            ))
    
    def update_layout(self, width, height, nticks):
        self.fig.update_xaxes(
            gridcolor="#1f292f",
            nticks=nticks,
        )

        self.fig.update_yaxes(
            gridcolor="#1f292f"
        )

        self.fig.update_layout(
            width=width,
            height=height,
            paper_bgcolor="#2c303c",
            plot_bgcolor="#2c303c",
            margin=dict(l=10,r=10,b=10,t=10),
            font=dict(size=8, color="#e1e1e1")
        )
    
    def show_plot(self, width=1600, height=900, nticks=5):
        self.update_layout(width, height, nticks)
        self.fig.show()