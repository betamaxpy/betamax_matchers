0.4.0 - 2017-01-16
------------------

- Remove support for python 3.2.
- Change json-body matcher to pass when the recorded request has the same
  content type as the issued request, and the content type is not json.
- Update ``JSONBodyMatcher`` to work with requests 2.11+.

0.3.0 - 2016-04-16
------------------

- Update for breaking changes in ``betamax`` 0.6.0

0.2.0 - 2015-06-17
------------------

- Add ``MultipartFormDataBodyMatcher``

0.1.0 - 2014-08-20
------------------

- Add ``JSONBodyMatcher``

- Add ``URLEncodedBodyMatcher``
