betamax_matchers
================

Experimental set of Matchers for `Betamax 
<https://github.com/sigmavirus24/betamax>`_ that may possibly end up in the 
main package.

JSON Body Matcher
-----------------

Usage::

    from betamax_matchers.json import JSONBodyMatcher

    from betamax import Betamax

    Betamax.register_request_matcher(JSONBodyMatcher)
