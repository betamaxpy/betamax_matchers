from requests_toolbelt.multipart import decoder

from betamax import BaseMatcher
from betamax.cassette.util import deserialize_prepared_request


class MultipartFormDataBodyMatcher(BaseMatcher):

    """A multipart/form-data body request matcher for Betamax."""

    name = 'multipart-form-data-body'

    def match(self, request, recorded_request):
        """Determine if the form encoded bodies match."""
        recorded = deserialize_prepared_request(recorded_request)

        # If neither of them have the right Content-Type set, return False
        request_content_type = request.headers.get('Content-Type')
        recorded_content_type = recorded.headers.get('Content-Type')
        if not (is_formdata(request_content_type) and
                is_formdata(recorded_content_type)):
            return False

        request_decoder = decoder.MultipartDecoder(request.body,
                                                   request_content_type)
        recorded_decoder = decoder.MultipartDecoder(recorded.body,
                                                    recorded_content_type)

        return decoders_equal(request_decoder, recorded_decoder)


def is_formdata(header):
    return header is not None and header == 'multipart/form-data'


def decoders_equal(request, recorded):
    if len(request.parts) != len(recorded.parts):
        return False

    parts = zip(request.parts, recorded.parts)
    return all(p1.content == p2.content for p1, p2 in parts)
