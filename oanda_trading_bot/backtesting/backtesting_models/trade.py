BUY = 1
SELL = -1
NONE = 0

class Trade:
    def __init__(self, row):
        self.open = True
        self.entry_price = row.entry_price
        self.take_profit = row.take_profit
        self.trade = row.trade
        self.pip_gain = 0.0
        self.open_time = row.time
        self.close_time = row.time
        self.duration = 0

        if self.trade == BUY:
            self.stop_loss = row.entry_price - 0.003
        
        if self.trade == SELL:
            self.stop_loss = row.entry_price + 0.003

        
    def tp_sl_check(self, row):
        if self.trade == 1:
            if row.mid_l >= self.take_profit:
                result = self.take_profit - self.entry_price
                self.close_trade(row, result)
            
            if row.mid_h >= (self.stop_loss):
                self.close_trade(row, -0.003)

        if self.trade == -1:
            if row.mid_h <= self.take_profit:
                result = self.entry_price - self.take_profit
                self.close_trade(row, result)

            if row.mid_l >= (self.stop_loss):
                self.close_trade(row, -0.003)


    def close_trade(self, row, result):
        self.running = False
        self.result = result
        self.end_time = row.time

        if row.trade == BUY:
            self.close_price = row.mid_l
        
        if row.trade == SELL:
            self.close_price = row.mid_h