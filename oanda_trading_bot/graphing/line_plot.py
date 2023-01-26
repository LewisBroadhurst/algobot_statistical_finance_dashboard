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
        self.fig.add_trace(go.scatter.Line(
            x=self.df_plot.sTime,
            y=self.df_plot.mid_c,
            mode='lines',
            name='lines'
        ))
    
    def show_plot(self, width=900, height=600, nticks=5):
        self.fig.show()