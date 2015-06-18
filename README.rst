betamax_matchers
================

Experimental set of Matchers for `Betamax 
<https://github.com/sigmavirus24/betamax>`_ that may possibly end up in the 
main package.

JSON Body Matcher
-----------------

Usage:

.. code-block:: python

    from betamax_matchers.json_body import JSONBodyMatcher

    from betamax import Betamax

    Betamax.register_request_matcher(JSONBodyMatcher)

Form URL Encoded Body Matcher
-----------------------------

Usage:

.. code-block:: python

    from betamax_matchers.form_urlencoded import URLEncodedBodyMatcher

    from betamax import Betamax

    Betamax.register_request_matcher(URLEncodedBodyMatcher)

Multipart Form Data Body Matcher
--------------------------------

Usage:

.. code-block:: python

    from betamax_matchers.multipart import MultipartFormDataBodyMatcher

    from betamax import Betamax

    Betamax.register_request_matcher(MultipartFormDataBodyMatcher)
