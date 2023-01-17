import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class CandlePlot:

    def __init__(self, df, candles = True):
        self.df_plot = df.copy()
        self.candles = candles
        self.create_candle_fig()

    def add_timestring(self):
        self.df_plot['sTime'] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df_plot.time]

    def create_candle_fig(self):
        self.add_timestring()
        self.fig = make_subplots(specs = [[{"secondary_y": True}]])

        if self.candles == True:
            self.fig.add_trace(go.Candlestick(
                x = self.df_plot.sTime,
                open = self.df_plot.mid_o,
                high = self.df_plot.mid_h,
                low = self.df_plot.mid_l,
                close = self.df_plot.mid_c,
                line = dict(width = 1), opacity = 1
            ))
    
    def update_layout(self, width, height, nticks):
        self.fig.update_xaxes(
            gridcolor = 'white',
            rangeslider = dict(visible = False),
            nticks = nticks
        )

        self.fig.update_yaxes(
            gridcolor = 'white'
        )

        self.fig.update_layout(
            width = width,
            height = height,
            margin = dict(l = 20, r = 20, b = 20, t = 20),
            font = dict(size = 8)
        )
    
    def add_traces(self, line_traces, is_secondary = False):
        for t in line_traces:
            self.fig.add_trace(go.Scatter(
            x = self.df_plot.sTime,
            y = self.df_plot[t],
            line = dict(width = 2),
            line_shape = "spline",
            name = t
        ), secondary_y = is_secondary)
    
    def show_plot(self, width=900, height=400, nticks=5, line_traces=[], secondary_traces=[]):
        self.add_traces(line_traces)
        self.add_traces(secondary_traces, is_secondary=True)
        self.update_layout(width, height, nticks)
        self.fig.show()