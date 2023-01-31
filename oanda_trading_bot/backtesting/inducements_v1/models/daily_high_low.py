class DailyHighLow:

    def __init__(self, time, price):
        self.taken = False
        self.expired = False
        self.time = time
        self.price = price

    def high_taken(self):
        self.taken = True

    def check_if_expired(self):
        self.expired = True