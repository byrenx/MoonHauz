from ferris import Controller
import json
import webapp2
from webob.exc import HTTPOk, HTTPRedirection
import logging


orig_dispatch = Controller.dispatch


def dispatch(self):
    try:
        orig_dispatch(self)
    except HTTPOk as e:
        raise e
    except HTTPRedirection as e:
        raise e
    except Exception as e:
        print e.__class__.__name__
        logging.exception(e)
        error_desc = e.description if hasattr(e, 'description') else repr(e)
        result = unicode(json.dumps(dict(message=error_desc)))
        resp = webapp2.Response()
        resp.charset = 'utf-8'
        resp.content_type = 'application/json'
        resp.status_int = e.code if hasattr(e, 'code') else 500
        resp.status_message = error_desc
        resp.unicode_body = result
        return resp


MoonHauzController = Controller
MoonHauzController.dispatch = dispatch
