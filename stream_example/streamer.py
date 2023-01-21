import json, threading, time
from api.stream_prices import PriceStreamer


def load_settings():

    with open("./bot/settings.json", "r") as f:
        return json.loads(f.read())


def run_streamer():

    settings = load_settings()
    shared_prices = {}
    shared_prices_events = {}
    shared_prices_lock = threading.Lock()

    for p in settings['pairs'].keys():
        shared_prices_events[p] = threading.Event()
        shared_prices_events[p] = {}
    
    threads = []

    price_stream_thread = PriceStreamer(shared_prices, shared_prices_lock, shared_prices_events)
    price_stream_thread.daemon = True

    threads.append(price_stream_thread)
    price_stream_thread.start()

    # for t in threads:
    #     t.join()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")

    print("ALL DONE")