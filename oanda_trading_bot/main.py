from api.stream_prices import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from stream_example.streamer import run_streamer

if __name__ == '__main__':
    api = OandaApi()    
    instrumentCollection.LoadInstruments("./candle_instrument_data")
    run_streamer()