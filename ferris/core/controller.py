import webapp2
import re
import weakref
from webapp2 import cached_property
from webapp2_extras import sessions
from google.appengine.api import users
from ferris.core.ndb import encode_key, decode_key
from ferris.core.uri import Uri
from ferris.core import inflector, auth, events, views, request_parsers, response_handlers, routing
from ferris.core.json_util import parse as json_parse, stringify as json_stringify
from bunch import Bunch


_temporary_route_storage = []


def route(f):
    """
    Marks a method for automatically routing and accessible via HTTP.
    See :mod:`~ferris.core.routing` for more details on how methods are auto-routed.
    This decorator should always be the outermost decorator.

    For example::

        @route
        def exterminate(self):
            return 'EXTERMINAAATE!'
    """
    global _temporary_route_storage
    _temporary_route_storage.append((f, (), {}))
    return f


def route_with(*args, **kwargs):
    """
    Marks a class method to be routed similar to :func:`route` and passes and additional arguments to the webapp2.Route
    constructor.

    :param template: Sets the URL template for this action


    For example::

        @route_with(template='/posts/archive/<year>')
        def archive_by_year(self, year):
            pass
    """
    def inner(f):
        _temporary_route_storage.append((f, args, kwargs))
        return f
    return inner


def add_authorizations(*args):
    """
    Adds additional authorization chains to a particular action. These are executed after the
    chains set in Controller.Meta.
    """
    def inner(f):
        setattr(f, 'authorizations', args)
        return f
    return inner


class Controller(webapp2.RequestHandler, Uri):
    """
    Controllers allows grouping of common actions and provides them with
    automatic routing, reusable components, request data parsering, and
    view rendering.
    """

    _controllers = []

    class __metaclass__(type):
        def __new__(meta, name, bases, dict):
            global _temporary_route_storage

            cls = type.__new__(meta, name, bases, dict)
            if name != 'Controller':
                # Add to the controller registry
                if not cls in Controller._controllers:
                    Controller._controllers.append(cls)

                # Make sure the metaclass as a proper inheritence chain
                if not issubclass(cls.Meta, Controller.Meta):
                    cls.Meta = type('Meta', (cls.Meta, Controller.Meta), {})

                cls._route_list = _temporary_route_storage
                _temporary_route_storage = []

            return cls

    # The name of this class, lowercase (automatically determined)
    name = 'controller'

    #: The current user as determined by ``google.appengine.api.users.get_current_user()``.
    user = None

    #: View Context, all these variables will be passed to the view.
    context = property(lambda self: self.meta.view.context)

    class Meta(object):
        """
        The Meta class stores configuration information for a Controller. This class is constructed
        into an instance and made available at ``self.meta``. This class is optional, Controllers that
        do not specify it will receive the default configuration. Additionally, you need not inherit from
        this class as Controller's metaclass will ensure it.

        For example::

            def Posts(Controller):
                class Meta:  # no inheritance
                    prefixes = ('admin', )
                    #  all other properties inherited from default.
        """

        #: List of components.
        #: When declaring a controller, this must be a list or tuple of classes.
        #: When the controller is constructed, ``controller.components`` will
        #: be populated with instances of these classes.
        components = tuple()

        #: Prefixes are added in from of controller (like admin_list) and will cause routing
        #: to produce a url such as '/admin/name/list' and a name such as 'admin:name:list'
        prefixes = tuple()

        #: Authorizations control access to the controller. Each authorization is a callable.
        #: Authorizations are called in order and all must return True for the request to be
        #: processed. If they return False or a tuple like (False, 'message'), the request will
        #: be rejected.
        #: You should **always** have ``auth.require_admin_for_prefix(prefix=('admin',))`` in your
        #: authorization chain.
        authorizations = (auth.require_admin_for_prefix(prefix=('admin',)),)

        #: Which :class:`~ferris.core.views.View` class to use by default. use :meth:`change_view` to switch views.
        View = views.TemplateView

        #: Which :class:`RequestParser` class to use by default. See :meth:`Controller.parse_request`.
        Parser = 'Form'

        def __init__(self, controller):
            self._controller = controller
            self.view = None
            self.change_view(self.View)

        def change_view(self, view, persist_context=True):
            """
            Swaps the view, and by default keeps context between the two views.

            :param view: View class or name.
            """
            context = self.view.context if self.view else None
            self.View = view if not isinstance(view, basestring) else views.factory(view)
            self.view = self.View(self._controller, context)

    class Util(object):
        """
        Provides some basic utility functions. This class is constructed into an instance
        and made available at ``controller.util``.
        """

        def __init__(self, controller):
            self._controller = controller

        #: Decodes a urlsafe ``ndb.Key``.
        decode_key = staticmethod(decode_key)

        #: Encode an ``ndb.Key`` (or ``ndb.Model`` instance) into an urlsafe string.
        encode_key = staticmethod(encode_key)

        #: Decodes a json string.
        parse_json = staticmethod(json_parse)

        #: Encodes a json string.
        stringify_json = staticmethod(json_stringify)

    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)

        self.name = inflector.underscore(self.__class__.__name__)
        self.proper_name = self.__class__.__name__
        self.util = self.Util(weakref.proxy(self))
        self.route = None

    def _build_components(self):
        self.events.before_build_components(controller=self)
        if hasattr(self.Meta, 'components'):
            component_classes = self.Meta.components
            self.components = Bunch()
            for cls in component_classes:
                if hasattr(cls, 'name'):
                    name = cls.name
                else:
                    name = inflector.underscore(cls.__name__)
                self.components[name] = cls(weakref.proxy(self))
        else:
            self.components = Bunch()
        self.events.after_build_components(controller=self)

    def _init_route(self):
        action = self.request.route.handler_method
        prefix = None
        for possible_prefix in self.Meta.prefixes:
            if action.startswith(possible_prefix):
                prefix = possible_prefix
                action = action.replace(prefix + '_', '')
                break

        self.route = Bunch(
            prefix=prefix,
            controller=self.name,
            action=action,
            name=self.request.route.name,
            args=self.request.route_args,
            kwargs=self.request.route_kwargs)

    def _init_meta(self):
        self.user = users.get_current_user()
        self._init_route()

        self.events = events.NamedBroadcastEvents(prefix='controller_')
        self.meta = self.Meta(weakref.proxy(self))
        self._build_components()

    @classmethod
    def _build_routes(cls, router):
        """
        Called in the main app router to get all of this controller's routes.
        Override to add custom/additional routes.
        """

        # Route the rest methods
        router.add(routing.build_scaffold_routes_for_controller(cls))
        for prefix in cls.Meta.prefixes:
            router.add(routing.build_scaffold_routes_for_controller(cls, prefix))

        # Auto route the remaining methods
        for route in routing.build_routes_for_controller(cls):
            vars = re.findall(r'\[(\w+)\]', route.template)
            if vars:
                action = route.handler_method
                split = action.split('_')
                prefixed = split[0] in cls.Meta.prefixes
                controller_data = {
                    'prefix': split[0] if prefixed else None,
                    'controller': inflector.underscore(cls.__name__),
                    'action': '_'.join(split[1:]) if prefixed else action,
                }

                for i in vars:
                    value = controller_data.get(i)
                    if not value:
                        continue
                    route.template = route.template.replace('['+i+']', value)
            router.add(route)

        events.fire('controller_build_routes', cls=cls, router=router)

    def startup(self):
        """
        Called when a new request is received and before authorization and dispatching.
        This is the main point in which to listen for events or change dynamic configuration.
        """
        pass

    def _is_authorized(self):
        authorizations = self.meta.authorizations

        #per-handler authorizations
        method = getattr(self, self.request.route.handler_method)
        if hasattr(method, 'authorizations'):
            authorizations = authorizations + method.authorizations

        authorizations = list(authorizations)  # convert to list so listeners can modify

        self.events.before_authorization(controller=self, authorizations=authorizations)

        auth_result = True

        for chain in authorizations:
            auth_result = chain(self)
            if auth_result is not True:
                break

        if isinstance(auth_result, webapp2.Response):
            pass

        elif auth_result is not True:
            message = u"Authorization chain rejected request"
            if isinstance(auth_result, tuple):
                message = auth_result[1]

            self.events.authorization_failed(controller=self, message=message)
            self.abort(403, message)

        self.events.after_authorization(controller=self, result=auth_result)

        return auth_result

    def _clear_redirect(self):
        if self.response.status_int in [300, 301, 302]:
            self.response.status = 200
            del self.response.headers['Location']

    def dispatch(self):
        """
        Calls startup, checks authorization, and then the controller method.

        If a view is set and auto rendering is enabled, then it will try to automatically
        render the view if the action doesn't return anything.

        If the controller method returns anything other than None, auto-rendering is skipped
        and the result is transformed into a response using the :mod:`~ferris.core.response_handlers`.
        """

        # Setup everything, the session, etc.
        self._init_meta()

        self.session_store = sessions.get_store(request=self.request)
        self.context.set_dotted('this.session', self.session)

        self.events.before_startup(controller=self)
        self.startup()
        self.events.after_startup(controller=self)

        # Authorization
        res = self._is_authorized()
        if isinstance(res, webapp2.Response):
            return res

        # Dispatch to the method
        self.events.before_dispatch(controller=self)
        result = super(Controller, self).dispatch()
        self.events.after_dispatch(response=result, controller=self)

        # Return value handlers.
        # Response has highest precendence, the view class has lowest.
        response_handler = response_handlers.factory(type(result))

        if response_handler:
            self.response = response_handler(self, result)

        # View rendering works similar to the string mode above.
        elif self.meta.view.auto_render:
            self._clear_redirect()
            self.response = self.meta.view.render()

        else:
            self.abort(500, 'Nothing was able to handle the response %s (%s)' % (result, type(result)))

        self.events.dispatch_complete(controller=self)

        self.session_store.save_sessions(self.response)
        self.events.clear()
        return self.response

    @cached_property
    def session(self):
        """
        Sessions are a simple dictionary of data that's persisted across requests for particular
        browser session.

        Sessions are backed by an encrypted cookie and memcache.
        """
        return self.session_store.get_session(backend='memcache')

    def parse_request(self, container=None, fallback=None, parser=None):
        """
        Parses request data (like GET, POST, JSON, XML) into a container (like a Form or Message)
        instance using a :class:`~ferris.core.request_parsers.RequestParser`. By default, it assumes
        you want to process GET/POST data into a Form instance, for that simple case you can use::

            data = self.parse_request()

        provided you've set the Form attribute of the Meta class.
        """
        parser_name = parser if parser else self.meta.Parser
        parser = request_parsers.factory(parser_name)

        if not container:
            container_name = parser.container_name
            if not hasattr(self.meta, container_name):
                raise AttributeError('Meta has no %s class, can not parse request' % container_name)
            container = getattr(self.meta, container_name)

        return parser.process(self.request, container, fallback)
