import json

from betamax import BaseMatcher

from ._compat import betamax_util as util


__all__ = ('JSONBodyMatcher',)


class JSONBodyMatcher(BaseMatcher):

    """A JSON body request matcher for Betamax."""

    name = 'json-body'

    def match(self, request, recorded_request):
        """Determine if the JSON encoded bodies match."""
        recorded = util.deserialize_prepared_request(recorded_request)

        recorded_type = recorded.headers.get('Content-Type')
        request_type = request.headers.get('Content-Type')
        # Short circuit fail when the content types do not match
        if recorded_type != request_type:
            return False
        # Short circuit pass when the content type is not json
        # This permits other matchers to do the matching on this body.
        if not is_json(recorded_type):
            return True

        if request.body:
            request_json = json.loads(util.coerce_content(request.body))
        else:
            request_json = None
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
