from api.oanda_api import OandaApi
from infrastructure.collect_data import run_collection
from infrastructure.instrument_collection import instrumentCollection as ic

api = OandaApi()
run_collection(ic, api)