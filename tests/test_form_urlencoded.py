"""Tests for the URLEncodedBodyMatcher."""
import pytest

from betamax.cassette.util import deserialize_prepared_request
from betamax_matchers.form_urlencoded import URLEncodedBodyMatcher


@pytest.fixture
def matcher():
    """Provide a URLEncodedBodyMatcher."""
    return URLEncodedBodyMatcher()


@pytest.fixture
def recorded_request():
    """Default recorded request."""
    return {
        'method': 'POST',
        'uri': 'https://httpbin.org/post',
        'body': {
            'string': 'foo=bar&biz=baz',
            'encoding': 'utf-8'
        },
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }


@pytest.fixture
def eq_request(recorded_request):
    """Provide a perfectly equal request."""
    return deserialize_prepared_request(recorded_request)


@pytest.fixture
def reversed_body_request():
    """Other recorded request."""
    return {
        'method': 'POST',
        'uri': 'https://httpbin.org/post',
        'body': {
            'string': 'biz=baz&foo=bar',
            'encoding': 'utf-8'
        },
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }


@pytest.fixture
def neq_request(recorded_request):
    """Provide a not equal request."""
    req = recorded_request.copy()
    req['body'] = {'string': '{}', 'encoding': 'utf-8'}
    return deserialize_prepared_request(req)


def test_equality(eq_request, recorded_request, matcher):
    """Assert that two requests with the same body will be equal."""
    assert matcher.match(eq_request, recorded_request) is True


def test_reversed_order_equality(eq_request, reversed_body_request, matcher):
    """Assert that two requests with equivalent bodies will be equal."""
    assert matcher.match(eq_request, reversed_body_request) is True


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

    eq_request.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    assert matcher.match(eq_request, recorded_request) is False
