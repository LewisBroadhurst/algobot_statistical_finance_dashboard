import datetime as dt
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

class CustomIndicator:

    def __init__(self, df: pd.DataFrame, indicator_traces: list):
        self.df_plot = df.copy()
        self.df_plot['sTime'] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df_plot.time]
        self.fig = go.Figure()
        self.fig = make_subplots(specs=[[{"secondary_y": True}]])

        for indicator_trace in indicator_traces:
            self.fig.add_trace(go.Line(
                x=self.df_plot.sTime,
                y=self.df_plot[f"{indicator_trace}"],
                mode='lines',
                name=f'{indicator_trace}'
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