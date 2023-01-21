import json
import requests

import constants.secrets as constants

STREAM_URL = f"https://stream-fxpractice.oanda.com/v3"

def stream_prices(pairs_list):
    params = dict(
        instruments = ','.join(pairs_list)
    )

    url = f"{STREAM_URL}/accounts/{constants.ACCOUNT_ID}/pricing/stream"

    response = requests.get(url, params, headers=constants.SECURE_HEADER, stream=True)

    for price in response.iter_lines():
        if price:
            decoded_price = json.loads(price.decode('utf-8'))
            print(decoded_price, "\n")