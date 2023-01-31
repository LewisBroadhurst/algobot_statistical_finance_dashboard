from api.stream_prices import OandaApi
from infrastructure.instrument_collection import instrumentCollection
import constants.secrets as constants
from stream_example.streamer import run_streamer

if __name__ == '__main__':
    api = OandaApi()    
    instrumentCollection.LoadInstruments("./data")
    run_streamer()