import functools
from time import sleep
import logging


def retries(max_tries, should_retry, delay=1, backoff=2):
    """
    Decorator that implements exponential backoff retry logic. If you have
    a function that may fail, this decorator can catch the exception and retry at
    exponentially increasing intervals until the number of retries is exhausted.

    The should_retry parameter should be a function that takes and exception as an argument
    and returns True if the function should be retried or False to permanently fail.

    This is extremely useful when working with external APIs. There is a shortcut
    decorator for working with Google APIs, see :func:`google_api_retries`.
    """
    def dec(func):
        functools.wraps(func)

        def f2(*args, **kwargs):
            seconds = delay
            tries = range(max_tries)
            tries.reverse()

            for tries_remaining in tries:
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    logging.info("Caught %s with %s retries left" % (e, tries_remaining))
                    if tries_remaining > 0 and should_retry(e):
                        logging.info("Exception raised, retrying in %s seconds" % seconds)
                        sleep(seconds)
                        seconds *= backoff
                    else:
                        raise e
                else:
                    break
        return f2
    return dec
