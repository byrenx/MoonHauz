"""
The App module provides the main WSGI app for ferris.
See /settings.py to configure the app. See app/routes.py
to configure routing
"""

import os
from webapp2 import WSGIApplication
from ferris.core import settings

# Only enable debug mode locally.
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

# Here's the main application, loads the config from the Ferris
# Settings API.
app = WSGIApplication(
    debug=debug,
    config=settings.get('app_config'))

# Custom Error Handlers
from ferris.controllers import errors
app.error_handlers[400] = errors.handle_400
app.error_handlers[401] = errors.handle_401
app.error_handlers[403] = errors.handle_403
app.error_handlers[404] = errors.handle_404
app.error_handlers[500] = errors.handle_500
