"""
Ferris' templating engine.
"""

from settings import settings
import logging
import os
import math
import datetime
import json
import jinja2
import webapp2
import types
import collections
from google.appengine.api import users, app_identity
from google.appengine.ext import db, ndb
import ferris.core
from ferris.core import events
from ferris.core import plugins
from ferris.core import time_util
from ferris.core.routing import route_name_exists, current_route_name
from ferris.core.json_util import DatastoreEncoder

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')


class TemplateEngine(object):

    def __init__(self, theme=None, extra_globals=None, extra_paths=None):
        self.theme = theme
        jinja2_env_kwargs = {
            'loader':      self._build_loader(extra_paths=extra_paths),
            'auto_reload': False,
            'cache_size':  0 if debug else 50,
        }
        events.fire('before_jinja2_environment_creation', engine=self, jinja2_env_kwargs=jinja2_env_kwargs)
        self.environment = jinja2.Environment(**jinja2_env_kwargs)
        events.fire('after_jinja2_environment_creation', engine=self)
        self._update_globals(extra_globals)
        events.fire("template_engine_created", self)

    def _build_loader(self, extra_paths=None):
        # Paths for resolving template file locations
        non_prefix_template_paths = [
            os.path.normpath(os.path.join(os.path.dirname(ferris.__file__), '../app/templates')),
            os.path.normpath(os.path.join(os.path.dirname(ferris.__file__), './templates'))
        ]
        prefix_paths = {
            'app': os.path.join(os.path.dirname(ferris.__file__), '../app/templates'),
            'ferris': os.path.join(os.path.dirname(ferris.__file__), './templates')
        }

        # Extra (plugin) paths
        if extra_paths:
            for x in extra_paths:
                if not x[1]:  # non prefixed
                    non_prefix_template_paths += x[0]

            prefix_paths.update({
                x[1]: x[0] for x in extra_paths if x[1]
            })

        # Theme Paths
        if self.theme:
            non_prefix_template_paths = [
                os.path.normpath(os.path.join(x, './themes/%s/' % self.theme))
                for x in non_prefix_template_paths
            ] + non_prefix_template_paths

        loader = jinja2.ChoiceLoader([
            jinja2.PrefixLoader({
                k: jinja2.FileSystemLoader(v)
                for k, v in prefix_paths.iteritems()}),
            jinja2.FileSystemLoader(non_prefix_template_paths)
        ])
        return loader

    def render(self, name, context=None):
        template = self.find(name)
        context = context if context else {}

        context.update({'template': {
            'name': template.name,
            'list': name,
            'theme': self.theme
        }})

        events.fire('before_template_render', name=name, context=context, env=self.environment)
        result = template.render(context, context=context)
        events.fire('after_template_render', result=result, name=name, context=context, env=self.environment)
        return result

    def find(self, name):
        return self.environment.get_or_select_template(name)

    def themed(self, name, theme=None):
        '''
        Returns a template from a particular theme, or the default.
        '''
        if theme:
            # Hilariously this works because our search paths always include the 'base',
            # so by just repeating what we do in determine paths, we can find a themed
            # version
            themed_name = '/themes/%s/%s' % (theme, name)
            try:
                return self.find(themed_name)
            except jinja2.TemplateNotFound:
                logging.debug('Template %s not found for theme %s' % (themed_name, theme))
                pass
        return self.find(name)

    def _update_globals(self, extra_globals=None):
        """
        Sets up all of the appropriate global variales for the templating system
        """

        self.environment.globals.update({
            'format_value': format_value,
            'isinstance': isinstance,
            'math': math,
            'int': int,
            'float': float,
            'round': round,
            'list': list,
            'str': str,
            'unicode': unicode,
            'datetime': datetime,
            'localize': time_util.localize,
            'ferris': {
                'format_value': format_value,
                'uri_for': webapp2.uri_for,
                'route_name_exists': route_name_exists,
                'current_route_name': current_route_name,
                'is_current_user_admin': users.is_current_user_admin,
                'users': users,
                'theme': self.theme,
                'settings': settings(),
                'has_plugin': plugins.exists,
                'plugins': plugins.list,
                'version': ferris.version,
                'app_version': os.environ['CURRENT_VERSION_ID'],
                'hostname': app_identity.get_default_version_hostname()
            },
            'json': _json_filter,
            'inflector': ferris.core.inflector,
            'dir': dir,
            'themed': self.themed.__get__(self),
            'ndb': ndb,
            'db': db,
        })
        self.environment.filters['json'] = _json_filter
        self.environment.tests['datetime'] = _is_datetime

        if extra_globals:
            self.environment.globals.update(extra_globals)


engines = {}

# This should not normally be used, global variables should not be dynamic,
# they can only be safely set when the app is first spun up before any
# templates are rendered. You should generally hook into a handler's
# before render callback.
global_context = {}

# Extra search paths, use add_template_path function for this.
extra_paths = []


def render_template(name, context=None, theme=None):
    """
    Renders the template given by name with the given context (variables).
    Uses the global context.
    """
    if context is None:
        context = {}

    return _get_engine(theme=theme).render(name, context)


def add_template_path(path_or_paths, prefix=None):
    """
    Used to add search paths to the template engine. Can only be called during application
    startup before any templates are rendered
    """
    global extra_paths
    if not isinstance(path_or_paths, list):
        path_or_paths = [path_or_paths]

    extra_paths.append((path_or_paths, prefix))


def _get_engine(theme=None):
    global engines
    global global_context
    global extra_paths

    if not theme in engines:
        engines[theme] = TemplateEngine(theme=theme, extra_globals=global_context, extra_paths=extra_paths)
    return engines[theme]

#
#   Filters
#


def _json_filter(obj, *args, **kwargs):
    """
    A filter to automatically encode a variable as json
    e.g. {{user|json}} renders {'email': 'something@something.com'}
    """
    return json.dumps(obj, *args, cls=DatastoreEncoder, **kwargs)


def _is_datetime(obj):
    return isinstance(obj, datetime.datetime)


#
# Formatters
#

formatters = {
    datetime.datetime: lambda x: time_util.localize(x).strftime('%b %d, %Y at %I:%M%p %Z'),
    datetime.date: lambda x: x.strftime('%b %d, %Y'),
    ndb.Key: lambda x: format_value(x.get())
}


def format_value(val):
    if isinstance(val, types.StringTypes):
        return val

    if isinstance(val, collections.Iterable):
        return u', '.join([format_value(x) for x in val])

    formatter = formatters.get(type(val))

    if formatter:
        return formatter(val)

    return unicode(val)
