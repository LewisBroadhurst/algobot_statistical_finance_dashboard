class DailyHighLow:

    def __init__(self, date, price):
        self.taken = False
        self.expired = False
        self.date = date
        self.price = price

    def high_taken(self):
        self.taken = True

    def check_if_expired(self):
        self.expired = True