import logging
import json
from ferris.core.template import render_template


def generic_handler(code, template=None):
    if not template:
        template = "%s" % code
    template = ('errors/%s.html' % template, 'errors/500.html')

    def inner(request, response, exception):
        logging.exception(exception)

        response.set_status(code)

        if 'application/json' in request.headers.get('Accept', []) or request.headers.get('Content-Type') == 'application/json':
            response.text = unicode(json.dumps({
                'error': str(exception),
                'code': code
            }, encoding='utf-8', ensure_ascii=False))

        else:
            response.content_type = 'text/html'
            response.text = render_template(template, {'request': request, 'exception': exception})

    return inner


handle_400 = generic_handler(400)
handle_401 = generic_handler(401)
handle_403 = generic_handler(403, '401')
handle_404 = generic_handler(404)
handle_500 = generic_handler(500)
