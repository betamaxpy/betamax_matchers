from requests_toolbelt.multipart import decoder

from betamax import BaseMatcher

from ._compat import betamax_util as util


class MultipartFormDataBodyMatcher(BaseMatcher):

    """A multipart/form-data body request matcher for Betamax."""

    name = 'multipart-form-data-body'

    def match(self, request, recorded_request):
        """Determine if the form encoded bodies match."""
        recorded = util.deserialize_prepared_request(recorded_request)

        # If neither of them have the right Content-Type set, return False
        request_content_type = request.headers.get('Content-Type')
        recorded_content_type = recorded.headers.get('Content-Type')
        if not (is_formdata(request_content_type) and
                is_formdata(recorded_content_type)):
            return False

        try:
            request_decoder = decoder.MultipartDecoder(
                request.body.encode('utf-8'),
                request_content_type
            )
            recorded_decoder = decoder.MultipartDecoder(
                recorded.body.encode('utf-8'),
                recorded_content_type
            )
        except decoder.ImproperBodyPartContentException:
            # If we can't parse on of these bodies, we probably don't want to
            # know anything about it.
            return False

        if len(request_decoder.parts) != len(recorded_decoder.parts):
            return False

        parts = zip(sorted_by_headers(request_decoder),
                    sorted_by_headers(recorded_decoder))
        for p1, p2 in parts:
            p1cd = p1.headers.get('Content-Disposition')
            p2cd = p2.headers.get('Content-Disposition')
            if (p1cd != p2cd or p1.content != p2.content):
                return False

        return True


def is_formdata(header):
    return header is not None and header.startswith('multipart/form-data')


def sorted_by_headers(decoder):
    def get_headers(part):
        return part.headers.get('Content-Disposition', '')

    return sorted(decoder.parts, key=get_headers)
