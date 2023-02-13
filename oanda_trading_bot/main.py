# from api.stream_prices import OandaApi
# from infrastructure.instrument_collection import instrumentCollection
# from stream_example.streamer import run_streamer
import pandas as pd

from charting.market_structure import MarketStructure

if __name__ == '__main__':
    # api = OandaApi()
    # instrumentCollection.LoadInstruments("./candle_instrument_data")
    # run_streamer()
    df = pd.read_pickle("candle_instrument_data/EUR_USD_M5.pkl")
    df = df.iloc[950000:950000]
    ms = MarketStructure(df)
    ms.run_simulation()
