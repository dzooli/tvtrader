import requests
import pytest
from pytest_bdd import when, then, given, scenarios
from pytest_bdd.parsers import parse

scenarios('features')


@pytest.fixture
def base_url():
    return "http://localhost:8089"


@given(parse('server available'))
def step_server_available(request, base_url):
    try:
        resp = requests.get(base_url)
    except Exception as ex:
        assert False, f"Connection failed: {str(ex)}!"
    assert resp is not None, "No response from the server"


@when(parse('GET "{route}" route'), target_fixture="resp")
def step_get_route(request, base_url, route, capsys):
    try:
        resp = requests.get(f"{base_url}{route}")
    except Exception:
        assert False, "Connection failed!"
    assert resp is not None, "Request failed!"
    return resp


@then(parse('message contains "{required_text}"'))
def step_message_contains(request, required_text, resp):
    assert "message" in resp.json().keys(), "Response message not found!"
    assert required_text in resp.json()["message"], \
        "Message content not found!"
