class TradeSettings:

    def __init__(self, object, pair):
        self.n_ma = object['n_ma']
        self.n_std = object['n_std']
        self.maxspread = object['maxspread']
        self.min_gain = object['min_gain']
        self.risk_reward = object['risk_reward']
    

    def __repr__(self):
        return str(vars(self))
    

    @classmethod
    def settings_to_str(cls, settings):
        return_string = "Trade Settings:\n"
        for _, v in settings.items():
            return_string += f"{v}\n"

        return return_string