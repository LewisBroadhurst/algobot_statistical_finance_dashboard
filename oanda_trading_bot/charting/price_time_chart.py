import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


class PriceTimeChart:

    def __init__(self, df: pd.DataFrame, chart_type: str):
        self.df_plot = df.copy()
        self.fig = go.Figure()
        self.chart_type = chart_type

        self.add_timestring()

        if chart_type is "candle":
            self.create_candle_fig()
        if chart_type is "line":
            self.create_line_fig()


    def add_timestring(self):
        """Hack for removing weekend candles"""
        self.df_plot['sTime'] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df_plot.time]


    def create_candle_fig(self):
        self.fig = make_subplots(specs=[[{"secondary_y": True}]])
        self.fig.add_trace(go.Candlestick(
            x=self.df_plot.sTime,
            open=self.df_plot.mid_o,
            high=self.df_plot.mid_h,
            low=self.df_plot.mid_l,
            close=self.df_plot.mid_c,
            line=dict(width=1), opacity=1,
            increasing_fillcolor='#24A06B',
            decreasing_fillcolor="#CC2E3C",
            increasing_line_color='#2EC886',
            decreasing_line_color='#FF3A4C'
        ))


    def create_line_fig(self, df_property):
        self.fig.add_trace(go.Line(
            x=self.df_plot.sTime,
            y=self.df_plot[df_property],
            mode='lines',
            name='price'
        ))


    def add_line_based_indicators(self, indicators: list):
        for indicator in indicators:
            self.fig.add_trace(go.Line(
                x=self.df_plot.sTime,
                y=self.df_plot[f"{indicator}"],
                mode='lines',
                name=f'{indicator}'
            ))


    # Show and Customise plot #


    def update_layout(self, width, height, ticks):
        self.fig.update_xaxes(
            gridcolor="#1f292f",
            nticks=ticks,
        )

        self.fig.update_yaxes(
            gridcolor="#1f292f"
        )

        self.fig.update_layout(
            width=width,
            height=height,
            paper_bgcolor="#2c303c",
            plot_bgcolor="#2c303c",
            margin=dict(l=10, r=10, b=10, t=10),
            font=dict(size=8, color="#e1e1e1")
        )


    def show_plot(self, width=1600, height=900, ticks=5):
        self.update_layout(width, height, ticks)
        self.fig.show()