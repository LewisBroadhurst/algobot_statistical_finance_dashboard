BUY = 1
SELL = -1
NONE = 0

class Trade:
    def __init__(self, row, entry_price, take_profit, stop_loss):
        self.running = True
        self.entry_price = entry_price
        self.take_profit = take_profit
        self.trade = row.trade
        self.result = 0.0
        self.start_time = row.time
        self.end_time = row.time
        self.duration = 0

        if self.trade == BUY:
            self.stop_loss = entry_price - 0.003
        
        if self.trade == SELL:
            self.stop_loss = entry_price + 0.003
        
    def close_trade(self, row, result):
        self.running = False
        self.result = result
        self.end_time = row.time

        if row.trade == BUY:
            self.close_price = row.mid_l
        
        if row.trade == SELL:
            self.close_price = row.mid_h
        
    def update(self, row):
        if self.trade == BUY:
            if row.mid_l >= self.take_profit:
                result = self.take_profit - self.entry_price
                self.close_trade(row, result)
            
            if row.mid_h >= (self.stop_loss):
                self.close_trade(row, -0.003)

        if self.trade == SELL:
            if row.mid_h <= self.take_profit:
                result = self.entry_price - self.take_profit
                self.close_trade(row, result)

            if row.mid_l >= (self.stop_loss):
                self.close_trade(row, -0.003)
