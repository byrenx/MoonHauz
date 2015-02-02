import template
import json_util
from protorpc import protojson
from protorpc.message_types import VoidMessage
from ferris.core.events import ViewEvents

_views = {}


def factory(name):
    """
    Creates a view instance by name
    """
    global _views
    return _views.get(name.lower(), _views.get((name + 'View').lower()))


class ViewContext(dict):
    def get_dotted(self, name, default=None):
        data = self
        path = name.split('.')
        for chunk in path[:-1]:
            data = data.setdefault(chunk, {})
        return data.setdefault(path[-1], default)

    def set_dotted(self, name, value):
        path = name.split('.')
        container = self.get_dotted('.'.join(path[:-1]), {})
        container[path[-1]] = value

    def set(self, **kwargs):
        self.update(**kwargs)


class View(object):

    class __metaclass__(type):
        def __new__(meta, name, bases, dict):
            global _views
            cls = type.__new__(meta, name, bases, dict)
            if name != 'View':
                _views[name.lower()] = cls
            return cls

    def __init__(self, controller, context=None):
        self.controller = controller
        self.auto_render = True

        if not context:
            context = ViewContext()
        if isinstance(context, dict) and not isinstance(context, ViewContext):
            context = ViewContext(**context)
        self.context = context

        self.events = ViewEvents(prefix='view')

    def render(self, *args, **kwargs):
        raise NotImplementedError("Base view can't render anything")


class TemplateView(View):

    def __init__(self, controller, context=None):
        super(TemplateView, self).__init__(controller, context)
        self.template_name = None
        self.template_ext = 'html'
        self.theme = None
        self.setup_template_variables()

    def setup_template_variables(self):
        self.context.get_dotted('this', {}).update({
            'route': self.controller.route,
            'name': self.controller.name,
            'uri': self.controller.uri,
            'uri_exists': self.controller.uri_exists,
            'on_uri': self.controller.on_uri,
            'request': self.controller.request,
            'self': self.controller,
            'encode_key': self.controller.util.encode_key,
            'decode_key': self.controller.util.decode_key,
            'user': self.controller.user,
            'events': self.events
        })
        self.context.update({
            'route': self.controller.route,
            'uri': self.controller.uri,
            'uri_exists': self.controller.uri_exists,
            'on_uri': self.controller.on_uri,
            'request': self.controller.request,
            'user': self.controller.user
        })
        self.controller.events.setup_template_variables(controller=self.controller)

    def render(self, *args, **kwargs):
        self.controller.events.before_render(controller=self.controller)

        result = template.render_template(self.get_template_names(), self.context, theme=self.theme)
        self.controller.response.content_type = 'text/html'
        self.controller.response.charset = 'utf-8'
        self.controller.response.unicode_body = result

        self.controller.events.after_render(controller=self.controller, result=result)

        return self.controller.response

    def get_template_names(self):
        """
        Generates a list of template names.

        The template engine will try each template in the list until it finds one.

        For non-prefixed actions, the return value is simply: ``[ "[controller]/[action].[ext]" ]``.
        For prefixed actions, another entry is added to the list : ``[ "[controller]/[prefix_][action].[ext]" ]``. This means that actions that are prefixed can fallback to using the non-prefixed template.

        For example, the action ``Posts.json_list`` would try these templates::

            posts/json_list.html
            posts/list.html

        """
        if self.template_name:
            return self.template_name

        templates = []

        template_path = "%s/" % self.controller.name
        action_name = "%s.%s" % (self.controller.route.action, self.template_ext)

        templates.append("%s%s" % (template_path, action_name))

        if self.controller.route.prefix:
            templates.insert(0, "%s%s_%s" % (template_path, self.controller.route.prefix, action_name))

        self.controller.events.template_names(controller=self.controller, templates=templates)

        return templates


class JsonView(View):

    def __init__(self, controller, context=None):
        super(JsonView, self).__init__(controller, context)
        self.variable_name = ('data',)

    def _get_data(self, default=None):
        self.variable_name = self.variable_name if isinstance(self.variable_name, (list, tuple)) else (self.variable_name,)

        if hasattr(self.controller, 'scaffold'):
            self.variable_name += (self.controller.scaffold.singular, self.controller.scaffold.plural)

        for v in self.variable_name:
            if v in self.context:
                return self.context.get(v)
        return default

    def render(self, *args, **kwargs):
        self.controller.events.before_render(controller=self.controller)

        result = unicode(json_util.stringify(self._get_data()))
        self.controller.response.content_type = 'application/json'
        self.controller.response.charset = 'utf-8'
        self.controller.response.unicode_body = result

        self.controller.events.after_render(controller=self.controller, result=result)

        return self.controller.response


class MessageView(JsonView):
    def render(self, *args, **kwargs):
        self.controller.events.before_render(controller=self.controller)

        data = self._get_data(default=VoidMessage())
        result = unicode(protojson.encode_message(data))
        self.controller.response.content_type = 'application/json'
        self.controller.response.charset = 'utf-8'
        self.controller.response.unicode_body = result

        self.controller.events.after_render(controller=self.controller, result=result)

        return self.controller.response
