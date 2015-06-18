import uuid

import pytest

from betamax.cassette.util import deserialize_prepared_request
from betamax_matchers import multipart


RECORDED_BODY = (
    '--{boundary}\r\n'
    'Content-Disposition: form-data; name="foo"\r\n\r\n'
    'bar\r\n--{boundary}\r\n'
    'Content-Disposition: form-data; name="biz"\r\n\r\n'
    'baz\r\n--{boundary}\r\n'
    'Content-Disposition: form-data; name="myfile.txt"; '
    'filename="myfile.txt"\r\n\r\n'
    'some contents of files\r\n'
    '--{boundary}--\r\n'
)


@pytest.fixture
def matcher():
    """Provide a JSONBodyMatcher."""
    return multipart.MultipartFormDataBodyMatcher()


@pytest.fixture
def recorded_request():
    """Default recorded request."""
    boundary = uuid.uuid4().hex
    return {
        'method': 'POST',
        'uri': 'https://httpbin.org/post',
        'body': {
            'string': RECORDED_BODY.format(boundary=boundary),
            'encoding': 'utf-8'
        },
        'headers': {
            'Content-Type': ('multipart/form-data; boundary='
                             '{boundary}'.format(boundary=boundary)),
        }
    }


@pytest.fixture
def eq_request(recorded_request):
    """Provide a perfectly equal request."""
    return deserialize_prepared_request(recorded_request)


@pytest.fixture
def neq_request(recorded_request):
    """Provide a not equal request."""
    rec = recorded_request.copy()
    rec['body'] = rec['body'].copy()
    body = recorded_request['body']['string']
    rec['body']['string'] = body.replace('baz', 'replaced')
    return deserialize_prepared_request(rec)


@pytest.fixture
def broken_request(recorded_request):
    recorded_request.copy()
    recorded_request['body']['string'] = '{"some": "json"}'
    return deserialize_prepared_request(recorded_request)


def test_equality(eq_request, recorded_request, matcher):
    """Assert that two requests with the same body will be equal."""
    assert matcher.match(eq_request, recorded_request) is True


def test_inequality(neq_request, recorded_request, matcher):
    """Assert that requests with different bodies will not be equal."""
    assert matcher.match(neq_request, recorded_request) is False


def test_broken_request(broken_request, recorded_request, matcher):
    """Assert that requests with unparseable bodies will not be equal."""
    assert matcher.match(broken_request, recorded_request) is False


def test_short_circuit_based_on_content_type(eq_request, recorded_request,
                                             matcher):
    """Assert that both require appropriate Content-Type headers."""
    del eq_request.headers['Content-Type']
    assert matcher.match(eq_request, recorded_request) is False

    del recorded_request['headers']['Content-Type']
    assert matcher.match(eq_request, recorded_request) is False

    eq_request.headers['Content-Type'] = 'application/json'
    assert matcher.match(eq_request, recorded_request) is False
