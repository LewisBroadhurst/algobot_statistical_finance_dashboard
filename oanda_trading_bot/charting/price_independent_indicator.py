import datetime as dt
import plotly.graph_objects as go
import pandas as pd


class PriceIndependentIndicator:

    def __init__(self, df: pd.DataFrame, base_indicator: str):
        self.df_plot = df.copy()
        self.fig = go.Figure()
        self.base_indicator = base_indicator

        self.add_timestring()
        self.create_line_fig(base_indicator)


    def add_timestring(self):
        """Hack for removing weekend candles"""
        self.df_plot['sTime'] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df_plot.time]


    def create_line_fig(self, base_indicator):
        self.fig.add_trace(go.Scatter(
            x=self.df_plot.sTime,
            y=self.df_plot[f'{base_indicator}'],
            mode='lines',
            name=f'{base_indicator}'
        ))


    def add_secondary_line_based_indicators(self, indicators: list):
        for indicator in indicators:
            self.fig.add_trace(go.Scatter(
                x=self.df_plot.sTime,
                y=self.df_plot[f"{indicator}"],
                mode='lines',
                name=f'{indicator}'
            ))

    def add_bar_based_indicators(self, indicators: list):
        for indicator in indicators:
            self.fig.add_trace(go.Bar(
                x=self.df_plot.sTime,
                y=self.df_plot[f"{indicator}"],
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