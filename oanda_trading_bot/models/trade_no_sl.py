BUY = 1
SELL = -1
NONE = 0

class TradeNoSL:
    def __init__(self, row, take_profit):
        self.running = True
        self.start_index = row.name
        self.take_profit = take_profit
        
        if row.trade == BUY:
            self.start_price = row.mid_l
            
        if row.SIGNAL == SELL:
            self.start_price = row.mid_h
            
        self.trade = row.trade
        self.result = 0.0
        self.start_time = row.time
        self.end_time = row.time
        self.duration = 0
        
    def close_trade(self, row, result):
        self.running = False
        self.result = result
        self.end_time = row.time
        if row.trade == 1:
            self.close_price = row.mid_l
        
        if row.trade == 0:
            self.close_price = row.mid_h
        
    def update(self, row):
        if self.trade == BUY:
            if row.bid_h >= self.TP:
                self.close_trade(row, self.take_profit, row.bid_h)

        if self.trade == SELL:
            if row.ask_l <= self.TP:
                self.close_trade(row, self.take_profit, row.ask_l)
