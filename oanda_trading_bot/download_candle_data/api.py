import requests
import pandas as pd
import json
from constants.secrets import API_KEY, OANDA_URL
import datetime as dt
from dateutil import parser


class OandaApi:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        })


    def make_request(self, url, params=None, data=None, headers=None):
        full_url = f"{OANDA_URL}/{url}"

        if data is not None:
            data = json.dumps(data)

        response = self.session.get(full_url, params=params, data=data, headers=headers)
        return response


    def fetch_candles(self, pair_name, date_f, date_t, granularity, price="MBA"):
        url = f"instruments/{pair_name}/candles"
        params = dict(
            granularity=granularity,
            price=price
        )

        date_format = "%Y-%m-%dT%H:%M:%SZ"
        params["from"] = dt.datetime.strftime(date_f, date_format)
        params["to"] = dt.datetime.strftime(date_t, date_format)

        data = self.make_request(url, params=params).json()
        print(data)
        return data['candles']




    def get_candles_df(self, pair_name, date_f, date_t, granularity):

        data = self.fetch_candles(pair_name, date_f, date_t, granularity)

        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']

        final_data = []
        for candle in data:
            if candle['complete'] is False:
                continue
            new_dict = {'time': parser.parse(candle['time']), 'volume': candle['volume']}
            for p in prices:
                if p in candle:
                    for o in ohlc:
                        new_dict[f"{p}_{o}"] = float(candle[p][o])
            final_data.append(new_dict)
        df = pd.DataFrame.from_dict(final_data)
        return df


# Candle Collection


def save_file(final_df: pd.DataFrame, file_prefix, granularity, pair, date_from, date_to):
    filename = f"{file_prefix}{pair}_{granularity}_20230208.pkl"

    final_df.drop_duplicates(subset=['time'], inplace=True)
    final_df.sort_values(by='time', inplace=True)
    final_df.reset_index(drop=True, inplace=True)
    final_df.to_pickle(filename)

    s1 = f"*** {pair} {granularity} {final_df.time.min()} {final_df.time.max()}"
    print(f"*** {s1} --> {final_df.shape[0]} candles ***")


def fetch_candles(pair, granularity, date_f: dt.datetime, date_t: dt.datetime, api: OandaApi):
    attempts = 0
    candles_df = None

    while attempts < 3:

        candles_df = api.get_candles_df(pair, date_f, date_t, granularity)

        if candles_df is not None:
            break

        attempts += 1

    if candles_df is not None and candles_df.empty is False:
        return candles_df
    else:
        return None


def collect_data(pair, granularity, date_f, date_t, file_prefix, api: OandaApi):
    end_date = parser.parse(date_t)
    from_date = parser.parse(date_f)

    candle_dfs = []

    to_date = from_date

    while to_date < end_date:
        to_date = from_date + dt.timedelta(minutes=3000)
        if to_date > end_date:
            to_date = end_date

        candles = fetch_candles(pair, granularity, from_date, to_date, api)

        if candles is not None:
            candle_dfs.append(candles)
            print(f"{pair} {granularity} {from_date} {to_date} --> {candles.shape[0]} candles loaded")
        else:
            print(f"{pair} {granularity} {from_date} {to_date} --> NO CANDLES")

        from_date = to_date

    if len(candle_dfs) > 0:
        final_df = pd.concat(candle_dfs)
        save_file(final_df, file_prefix, granularity, pair, date_f, date_t)


def run_collection(api: OandaApi):
    for pair in ["EUR_USD"]:
        for granularity in ["M1"]:
            print(pair, granularity)
            collect_data(pair, granularity, "2023-01-28T00:00:00Z", "2023-02-08T19:00:00Z", "./", api)