from dateutil import parser

class OpenTrade:

    def __init__(self, api_object):
        self.id = api_object['id']
        self.instrument = api_object['instrument']
        self.price = float(api_object['price'])
        self.currentUnits = float(api_object['currentUnits'])
        self.unrealizedPL = float(api_object['unrealizedPL'])
        self.marginUsed = float(api_object['marginUsed'])
    

    def __repr__(self):
        return str(vars(self))