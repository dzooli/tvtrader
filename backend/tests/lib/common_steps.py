import requests
from pprint import pprint
from pytest_bdd import when, then, given, parsers


@given(parsers.parse("server available"))
def step_server_available(base_url: str) -> None:
    """
    Check if server is responsible

    Args:
        base_url (str): Server health endpoint
    """
    resp = None
    try:
        resp = requests.get(base_url)
    except Exception as ex:
        assert False, f"Connection failed: {str(ex)}!"
    assert resp is not None, "No response from the server"


@when(parsers.parse('GET "{route}" route'), target_fixture="response")
def step_get_route(base_url, route) -> requests.Response:
    """GET the route

    Args:
        base_url str:   API endpoint base
        route str:      Rest of the endpoint

    Returns:
        requests.Response: Response from the server
    """
    resp = None
    try:
        resp = requests.get(f"{base_url}{route}")
    except Exception:
        assert False, "Connection failed!"
    assert resp is not None, "Request failed!"
    return resp


@then(parsers.parse("response code is {code:d}"))
def step_resp_code_is(code: int, response: requests.Response) -> None:
    """Check the response code

    Args:
        code (int): expected response code
        response (requests.Response): Target response of the check
    """
    assert isinstance(response, requests.Response)
    pprint(response.json())
    pprint(response.request.body)
    assert (
        response.status_code == code
    ), f"Got unexpected response code {response.status_code} (expected: {code})"


@then(parsers.parse('message contains "{required_text}"'))
def step_message_contains(required_text: str, response: requests.Response) -> None:
    """Check the response body for a given string

    Args:
        required_text (str): Text to check for
        response (requests.Response): Target response of the check
    """
    assert "message" in response.json().keys(), "Response message not found!"
    assert required_text in response.json()["message"], "Message content not found!"


@then("response dumped")
def step_dump_response(response, capsys) -> None:
    """Dump response JSON

    Usable for debugging.

    Args:
        response (requests.Response): Target response of the check
        capsys (pytest.Fixture): System message capturing
    """
    with capsys.disabled():
        print(f"Response dump: {response.json()}")
