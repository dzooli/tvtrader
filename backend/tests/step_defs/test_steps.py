import requests
import json
from pytest_bdd import when, then, given, scenarios, parsers

from ..lib.fixtures import base_url
from ..lib.common_steps import *
from ..lib.common_functions import asdict
from src.schemas.alerts import TradingViewAlert

scenarios('../features')


@given(parsers.parse('alert with {id:n}, {name}, {symbol}, {interval:d}, {direction}, {price:f}, {timestamp}'), target_fixture="prepared_alert")
def step_prepare_alert(id, name, symbol, interval, direction, price, timestamp):
    alert = TradingViewAlert(id, name, symbol, interval,
                             direction, price, timestamp)
    return alert


@given(parsers.parse('{fieldname}:{num_or_str} field is {miss_or_inv}'), target_fixture="prepared_alert")
def step_remove_field(prepared_alert, fieldname, num_or_str="n", miss_or_inv="missing"):
    alert = asdict(prepared_alert)
    if miss_or_inv == "missing":
        del alert[fieldname]
    else:
        alert[fieldname] = -1 if num_or_str == "n" else ""
    return alert


@when(parsers.parse('sending the prepared alert to endpoint: {endpoint}'), target_fixture="response")
def step_send_prepared(base_url, prepared_alert, endpoint):
    send_alert = prepared_alert
    if isinstance(prepared_alert, TradingViewAlert):
        send_alert = asdict(prepared_alert)
    return requests.post(f"{base_url}/{endpoint}", json=send_alert)
