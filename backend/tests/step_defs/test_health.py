import requests
import pytest
from pytest_bdd import when, then, given, scenarios
from pytest_bdd.parsers import parse

from ..lib.fixtures import base_url
from ..lib.common_steps import *

scenarios('../features')


@when(parse('GET "{route}" route'), target_fixture="response")
def step_get_route(base_url, route, capsys):
    try:
        resp = requests.get(f"{base_url}{route}")
    except Exception:
        assert False, "Connection failed!"
    assert resp is not None, "Request failed!"
    return resp


@then(parse('message contains "{required_text}"'))
def step_message_contains(required_text, response):
    assert "message" in response.json().keys(), "Response message not found!"
    assert required_text in response.json()["message"], \
        "Message content not found!"
