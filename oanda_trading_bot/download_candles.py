from api.oanda_api import OandaApi
from infrastructure.collect_data import run_collection
import json


api = OandaApi()
f = open("data/instruments.json")
data = json.load(f)
run_collection(data, api)
f.close()