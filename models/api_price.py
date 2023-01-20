
class ApiPrice:

    def __init__(self, api_ob, homeConversions):
        self.instrument = api_ob['instrument']
        self.ask = float(api_ob['asks'][0]['price'])
        self.bid = float(api_ob['bids'][0]['price'])

        base_instrument = self.instrument.split('_')[1]
        for hc in homeConversions:
            if hc['currency'] == base_instrument:
                self.sell_conv = float(hc['positionValue'])
                self.buy_conv = float(hc['positionValue'])

    def __repr__(self):
        return f"ApiPrice() {self.instrument} {self.ask} {self.bid} {self.sell_conv:.5f} {self.buy_conv:.5f}"
