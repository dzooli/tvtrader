from pytest_bdd import when, then, given, parsers
import requests


@given(parsers.parse('server available'))
def step_server_available(base_url):
    resp = None
    try:
        resp = requests.get(base_url)
    except Exception as ex:
        assert False, f"Connection failed: {str(ex)}!"
    assert resp is not None, "No response from the server"


@then(parsers.parse('response code is {code:d}'))
def step_resp_code_is(code, response: requests.Response):
    assert response and response.status_code == code, f"Got unexpected response code {response.status_code} (expected: {code})"
