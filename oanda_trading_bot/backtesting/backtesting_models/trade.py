

class Trade:
    def __init__(self, row, tp_func, sl_func):
        self.time = row.time
        self.open = True

        if row.trade == 1:
            self.entry_price = row.mid_c
        if row.trade == -1:
            self.entry_price = row.mid_c

        self.tp = tp_func(row)
        self.sl = sl_func(row)
        self.trade = row.trade
        self.pip_gain = 0.0

        
    def tp_sl_check(self, row):
        if self.trade == 1:
            if row.mid_c >= self.tp:
                self.close_trade(row, "W")
            
            if row.mid_c <= self.sl:
                self.close_trade(row, "L")

        if self.trade == -1:
            if row.mid_c <= self.tp:
                self.close_trade(row, "W")
            
            if row.mid_c >= self.sl:
                self.close_trade(row, "L")


    def close_trade(self, row, outcome):
        self.open = False
        self.close_time = row.time

        if row.trade == 1:
            if outcome == "W":
                self.close_price = self.tp
                self.pip_gain = self.tp - self.entry_price
            
            if outcome == "L":
                self.close_price = self.sl
                self.pip_gain = self.sl - self.entry_price
        
        
        if row.trade == -1:
            if outcome == "W":
                self.close_price = self.tp
                self.pip_gain = self.entry_price - self.tp
            
            if outcome == "L":
                self.close_price = self.sl
                self.pip_gain = self.entry_price - self.sl