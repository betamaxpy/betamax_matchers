import json

from betamax import BaseMatcher
from betamax.cassette.util import deserialize_prepared_request


__all__ = ('JSONBodyMatcher',)


class JSONBodyMatcher(BaseMatcher):

    """A JSON body request matcher for Betamax."""

    name = 'json-body'

    def match(self, request, recorded_request):
        """Determine if the JSON encoded bodies match."""
        recorded = deserialize_prepared_request(recorded_request)

        # If neither of them have the right Content-Type set, return False
        if not (is_json(request.headers.get('Content-Type')) and
                is_json(recorded.headers.get('Content-Type'))):
            return False

        request_json = json.loads(request.body) if request.body else None

        recorded_json = json.loads(recorded.body) if recorded.body else None

        return request_json == recorded_json


def is_json(content_type):
    """Simplistic check for a JSON Content-Type.

    This will handle header values like::

        application/json
        application/vnd.github.v3.full+json

    """
    content_type = content_type or ''
    return content_type.startswith('application/') and 'json' in content_type
