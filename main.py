from api.oanda_api import OandaApi
from infrastructure.instrument_collection import instrumentCollection
from simulation.ma_cross import run_ma_sim
from simulation.ema_macd_start import run_ema_macd
from dateutil import parser
from infrastructure.collect_data import run_collection

if __name__ == '__main__':
    # api = OandaApi()
    # run_collection(instrumentCollection, api)

    instrumentCollection.LoadInstruments("./data")
    run_ema_macd(instrumentCollection)