from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from models.candle_timing import CandleTiming

if __name__ == '__main__':
    api = OandaApi()
    instrumentCollection.LoadInstruments("./data")
    
    dd = api.last_complete_candle("EUR_USD", granularity="M5")
    print(CandleTiming(dd))