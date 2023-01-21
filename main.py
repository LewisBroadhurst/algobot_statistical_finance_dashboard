from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from api.stream_prices import stream_prices
import constants.secrets as constants

if __name__ == '__main__':
    api = OandaApi()    
    instrumentCollection.LoadInstruments("./data")
    stream_prices(["BTC_USD"])
    