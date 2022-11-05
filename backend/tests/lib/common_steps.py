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
    assert isinstance(response, requests.Response)
    assert response.status_code == code, f"Got unexpected response code {response.status_code} (expected: {code})"


@then(parsers.parse('message contains "{required_text}"'))
def step_message_contains(required_text, response):
    assert "message" in response.json().keys(), "Response message not found!"
    assert required_text in response.json()["message"], \
        "Message content not found!"


@then('response dumped')
def step_dump_response(response, capsys):
    with capsys.disabled():
        print(f"Response dump: {response.json()}")
