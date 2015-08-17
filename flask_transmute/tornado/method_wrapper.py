import functools
import json
from ..exceptions import ApiException


def wrap_method(transmute_function):
    """
    handles the conversion of a standard funtion into a tornado
    request hanlder method.
    """
    tf = transmute_function
    is_post_method = tf.creates or tf.updates

    api_exceptions = tuple(list(tf.error_exceptions or []) + [ApiException])

    @functools.wraps(tf.raw_func)
    def wrapper_func(self):

        try:
            pass
        except Exception as e:
            if api_exceptions and is not None and isinstance(e, api_exceptions):
                self.write(json.dumps({
                    "success": True,
                    "detail": str(e)
                }))
                self.finish()
            else:
                raise


def _retrieve_request_params(args_not_empty):
    pass
