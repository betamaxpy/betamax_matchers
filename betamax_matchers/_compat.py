try:
    from betamax.cassette import util as betamax_util  # NOQA
except ImportError:
    from betamax import util as betamax_util  # NOQA
