import httplib2
import logging
import json
import functools
from apiclient import discovery, errors
import hashlib


def build(serviceName, version, credentials):
    """
    Build a Google API client and caches it in the in-process cache. This reduces
    the number of calls to the discovery API as well as making it easy to share
    the client across multiple parts of code with little effort.

    Usage is exactly like apiclient.discovery.build::

        drive = build("drive", "v2", credentials)

    """
    from ferris import caching
    credentials_hash = hashlib.sha1(credentials.to_json()).hexdigest()
    cache_key = "ferris:google-client-%s-%s-%s" % (serviceName, version, credentials_hash)

    @caching.cache_using_local(cache_key)
    def inner():
        http = httplib2.Http()
        credentials.authorize(http)
        service = discovery.build(serviceName, version, http=http)
        return service

    return inner()


def retry_execute(request):
    """
    Executes the given request from the Google API client and applies the
    appropriate retry policy. This ensures that if your request fails due to
    internal server error or quota denial the request will be automatically
    retried.

    Example::

        request = service.files().list()
        result = retry_execute(request)

    """
    @retries
    def inner():
        return request.execute()
    return inner()


def retries(f):
    """
    Shortcut decorator that uses the appropraite retry policy for dealing with Google APIs.

    Will retry if an HttpError in the 5xx range is raise, but will fail if the error is in the 4xx range.

    This is useful over retry_execute because it can retry an entire function, not just a single request.

    Example::

        @retries
        def rename_file():
            client = build('drive', 'v2')
            client.files().update(fileId="123", data={"name": "Test"}).execute()

    """
    from ferris import retries as ferris_retries

    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except errors.HttpError as error:
            raise
        except Exception as error:
            logging.error("Non-recoverable exception: %s" % error)
            raise

    r_inner = ferris_retries(max_tries=5, should_retry=apiclient_retry_policy, delay=1, backoff=2)(inner)
    return r_inner


def apiclient_retry_policy(exception):
    if not isinstance(exception, errors.HttpError):
        return False

    try:
        error = json.loads(exception.content)
        error = error.get('error', error)
        code = error.get('code')
        reason = error.get('errors', [{}])[0].get('reason')
        if code == 403 and reason in ('rateLimitExceeded', 'userRateLimitExceeded'):
            logging.info("Rate limit exceeded, retrying...")
            return True
        elif code == 403 and reason in ('dailyLimitExceeded',):
            logging.error("Uh oh- daily quota limit exceeded!")
            return False
        elif code == 403:
            logging.info("I think the rate limit was exceeded (reason was %s), so retrying..." % reason)
            return True
        else:
            logging.info("Non-rate limit API error %s raised" % error.get('message'))

    except ValueError:
        logging.error("Failed to parse json from exception: %s" % exception.content)

    return False


def get_discovery_document(api, api_version, uri_template="https://www.googleapis.com/discovery/v1/apis/{api}/{api_version}/rest", http=None):
    """
    Provides an automatic caching version of the apiclient discovery
    document fetching mechanism using memcache.
    """
    from ferris import caching
    if not http:
        http = httplib2.Http()

    uri = uri_template.format(api=api, api_version=api_version)

    @caching.cache_using_memcache('gapi-discovery-doc-%s' % uri, 24*60*60)
    def fetch():
        r, c = http.request(uri)
        return r, c

    r, c = fetch()

    return c


def patch_discovery():
    original_build = discovery.build

    def patched_build(serviceName, version, http=None, **kwargs):
        doc = get_discovery_document(serviceName, version, http=http)
        return discovery.build_from_document(doc, http=http, **kwargs)

    discovery.build = patched_build
    setattr(discovery, '_build', original_build)


patch_discovery()
