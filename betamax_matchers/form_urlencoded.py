"""
Implementation logic for the application/x-www-form-urlencoded request body.

To use this matcher::

    import requests

    from betamax import Betamax
    from betamax_matchers.form_urlencoded import URLEncodedBodyMatcher

    Betamax.register_request_matcher(URLEncodedBodyMatcher)

    def test_urlencoded_body():
        s = requests.Session()
        m = ['method', 'uri', 'form-urlencoded-body']
        with Betamax(s).use_cassette('urlencoded', match_requests_on=m):
            r = s.post('https://httpbin.org/post', data={
                'form-field-0': 'value-0',
                'form-field-1': 'value-1',
                'form-field-2': 'value-2',
            })

"""
try:
    from urlparse import parse_qs  # Python 2
except ImportError:
    from urllib.parse import parse_qs  # Python 3

from betamax import BaseMatcher
from betamax.cassette.util import deserialize_prepared_request


__all__ = ('URLEncodedBodyMatcher',)


class URLEncodedBodyMatcher(BaseMatcher):

    """A x-www-form-urlencoded body request matcher for Betamax."""

    name = 'form-urlencoded-body'

    def match(self, request, recorded_request):
        """Determine if the form encoded bodies match."""
        recorded = deserialize_prepared_request(recorded_request)

        # If neither of them have the right Content-Type set, return False
        if not (is_form(request.headers.get('Content-Type')) and
                is_form(recorded.headers.get('Content-Type'))):
            return False

        request_form = parse_qs(request.body) if request.body else None

        recorded_form = parse_qs(recorded.body) if recorded.body else None

        return request_form == recorded_form


def is_form(content_type):
    """Simplistic check for a x-www-form-urlencoded Content-Type.

    This will handle header values like::

        application/x-www-form-urlencoded

    """
    content_type = content_type or ''
    return (content_type.startswith('application/') and
            'x-www-form-urlencoded' in content_type)
