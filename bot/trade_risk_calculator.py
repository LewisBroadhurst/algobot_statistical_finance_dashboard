from api.oanda_api import OandaApi
import constants.secrets as constant
from infrastructure.instrument_collection import instrumentCollection as ic


def get_trade_units(api: OandaApi, pair, signal, loss, trade_risk, log_message):

    prices = api.get_prices([pair])

    if prices is None or len(prices) == 0:
        log_message("get_trade_units() Prices is none", pair)
        return False

    price = None
    for p in prices:
        if p.instrument == pair:
            price = p
            break

    if price is None:
        log_message("get_trade_units() price is None????", pair)
        return False

    log_message(f"get_trade_units() price {price}", pair)

    conv = price.buy_conv
    if signal == constant.SELL:
        conv = price.sell_conv

    pip_location = ic.instruments_dict[pair].pipLocation
    num_pips = loss / pip_location
    per_pip_loss = trade_risk / num_pips
    units = per_pip_loss / (conv * pip_location)

    log_message(f"{pip_location} {num_pips} {per_pip_loss} {units:.1f}", pair)

    return units
