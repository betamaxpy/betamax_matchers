import pytest

from betamax_matchers._compat import betamax_util as util
from betamax_matchers.json_body import JSONBodyMatcher


@pytest.fixture
def matcher():
    """Provide a JSONBodyMatcher."""
    return JSONBodyMatcher()


@pytest.fixture
def recorded_request():
    """Default recorded request."""
    return {
        'method': 'POST',
        'uri': 'https://httpbin.org/post',
        'body': {
            'string': '{"hello": "world"}',
            'encoding': 'utf-8'
        },
        'headers': {
            'Content-Type': 'application/json'
        }
    }


@pytest.fixture
def eq_request(recorded_request):
    """Provide a perfectly equal request."""
    return util.deserialize_prepared_request(recorded_request)


@pytest.fixture
def neq_request(recorded_request):
    """Provide a not equal request."""
    req = recorded_request.copy()
    req['body'] = {'string': '{}', 'encoding': 'utf-8'}
    return util.deserialize_prepared_request(req)


def test_equality(eq_request, recorded_request, matcher):
    """Assert that two requests with the same body will be equal."""
    assert matcher.match(eq_request, recorded_request) is True


def test_inequality(neq_request, recorded_request, matcher):
    """Assert that requests with different bodies will not be equal."""
    assert matcher.match(neq_request, recorded_request) is False


def test_short_circuit_based_on_content_type(eq_request, recorded_request,
                                             matcher):
    """Assert that both require appropriate Content-Type headers."""
    del eq_request.headers['Content-Type']
    assert matcher.match(eq_request, recorded_request) is False

    del recorded_request['headers']['Content-Type']
    assert matcher.match(eq_request, recorded_request) is False

    eq_request.headers['Content-Type'] = 'application/json'
    assert matcher.match(eq_request, recorded_request) is False
