LEGACY_USAGE_ERROR = """
looks like you are attempting to
use a function in the pre-1.0
flask-transmute, which is no longer
supported.

The last pre-1.0 release is 0.2.15. You
can pin to that, or upgrade to the new
syntax and approach:

http://flask-transmute.readthedocs.io/en/latest/legacy/migrating.html
http://transmute-core.readthedocs.io/en/latest/
""".strip()


def FlaskRouteSet(*args, **kwargs):
    raise NotImplementedError(LEGACY_USAGE_ERROR)


def Swagger(*args, **kwargs):
    raise NotImplementedError(LEGACY_USAGE_ERROR)
