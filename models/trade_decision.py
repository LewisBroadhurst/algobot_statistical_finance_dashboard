class TradeDecision:

    def __init__(self, row):
        self.gain = row.GAIN
        self.SIGNAL = row.SIGNAL
        self.sl = row.SL
        self.tp = row.TP
        self.pair = row.PAIR

    def __repr__(self):
        return f"TradeDecision: {self.gain} {self.SIGNAL} {self.sl} {self.tp} {self.pair}"