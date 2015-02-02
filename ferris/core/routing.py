"""
Ferris' routing utilities
"""

import os
import inspect
import webapp2
import logging
import ferris
from ferris.core import inflector
from webapp2 import Route
from webapp2_extras import routes


def get_true_name_and_argspec(method):
    """
    Drills through layers of decorators attempting to locate
    the actual argspec for the method.
    """

    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args and args[0] == 'self':
        return method.__name__, argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, 'func_closure') or method.func_closure is None:
        raise Exception("No closure for method.")

    method = method.func_closure[0].cell_contents
    return get_true_name_and_argspec(method)


def router():
    return ferris.app.app.router


def add(route, app_router=None):
    """
    Adds a webapp2.Route class to the router
    """
    if not app_router:
        app_router = router()
    app_router.add(route)


def auto_route(app_router=None, plugin=None):
    """
    Automatically routes all controllers in main app or the given plugin
    """
    if not app_router:
        app_router = router()
    route_all_controllers(app_router, plugin=None)


def redirect(url, to, app_router=None):
    """
    Adds a redirect route with the given url templates.
    """
    add(routes.RedirectRoute(url, redirect_to=to), app_router)


def default_root(app_router=None):
    """
    Adds the default Ferris root route
    """
    from ferris.controllers.root import Root
    add(Route('/', Root, handler_method='root'), app_router)


def route_all_controllers(app_router, plugin=None):
    """
    Called in app.routes to automatically route all controllers in the app/controllers
    folder
    """
    base_directory = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..', '..'))
    directory = os.path.join('app', 'controllers')
    if plugin:
        directory = os.path.join('plugins', plugin, 'controllers')

        # import the root plugin module first, this enables all templates and listeners
        plugin_module = __import__('plugins.%s' % plugin, fromlist=['*'])
        (plugin_module)

    directory = os.path.join(base_directory, directory)
    # the length of the path before "app/controllers"
    base_directory_path_len = len(base_directory.split(os.path.sep))
    
    # check if [base_directory]/app/controllers exists
    if not os.path.exists(directory):
        return

    # walk the app/controllers directory and sub-directories
    for root_path, _, files in os.walk(directory):
        for file in files:
            partial_path = root_path.split(os.path.sep)[base_directory_path_len:]
            if file.endswith(".py") and file != '__init__.py':
                try:
                    name = file.split('.')[0]
                    module_path = '.'.join(partial_path)
                    if plugin:
                        module_path = 'plugins.%s.controllers' % plugin
                    module = __import__('%s.%s' % (module_path, name), fromlist=['*'])

                    try:
                        cls = getattr(module, inflector.camelize(name))
                        route_controller(cls, app_router)

                    except AttributeError:
                        logging.debug("Controller %s not found, skipping" % inflector.camelize(name))

                except AttributeError as e:
                    logging.error('Thought %s was a controller, but was wrong (or ran into some weird error): %s' % (file, e))
                    raise


def route_controller(controller_cls, app_router=None):
    """
    Adds all of the routes for the given controller
    """
    if not app_router:
        app_router = router()

    return controller_cls._build_routes(app_router)


def route_name_exists(name, *args, **kwargs):
    """
    Checks if a particlar named route (i.e. 'entries-list') exists.
    """
    route = webapp2.get_app().router.build_routes.get(name)
    return True if route else False


def current_route_name():
    """
    Gets the name (i.e. 'entries-list') from the router.
    """
    name = webapp2.get_app().request.route.name
    return name


def canonical_parts_from_method(controller, method):
    """
    Returns the canonical parts (prefix, controller, action, named arguments)
    from a controller's method
    """
    method_name, method_args = get_true_name_and_argspec(method)
    method_class = controller
    method_class_name = inflector.underscore(method_class.__name__)
    prefix = None

    if hasattr(method_class, 'Meta'):
        prefixes = method_class.Meta.prefixes
    else:
        prefixes = method_class.prefixes

    for tprefix in prefixes:
        if method_name.startswith(tprefix + '_'):
            prefix = tprefix
            method_name = method_name.replace(prefix + '_', '')

    return {
        'prefix': prefix,
        'controller': method_class_name,
        'action': method_name,
        'args': method_args.args[1:]  # exclude self
    }


def path_from_canonical_parts(prefix, controller, action, args):
    """
    Returns a route ('/admin/users/edit/3') from canonical parts
    ('admin', 'users', 'edit', [id])
    """
    args_parts = ['<' + x + '>' for x in args]
    route_parts = [prefix, controller, action] + args_parts
    route_parts = [x for x in route_parts if x]
    route_path = '/' + '/'.join(route_parts)

    return route_path


def name_from_canonical_parts(prefix, controller, action, args=None):
    """
    Returns the route's name ('admin-users-edit') from the canonical
    parts ('admin','users','edit')
    """
    route_parts = [prefix, controller, action]
    route_parts = [x for x in route_parts if x]
    route_name = ':'.join(route_parts)

    return route_name


def build_routes_for_controller(controllercls):
    """
    Returns list of routes for a particular controller, to enable
    methods to be routed, add the ferris.core.controller.auto_route
    decorator, or simply set the 'route' attr of the function to
    True.

    def some_method(self, arg1, arg2, arg3)

    becomes

    /controller/some_method/<arg1>/<arg2>/<arg3>
    """
    routes_list = []
    name_counters = {}

    for entry in controllercls._route_list:
        method = entry[0]
        args = entry[1]
        kwargs = entry[2]

        parts = canonical_parts_from_method(controllercls, method)
        route_path = path_from_canonical_parts(**parts)
        route_name = name_from_canonical_parts(**parts)

        # not the most elegant way to determine the
        # correct member name, but it works. Alternatively,
        # i could use get_real_name_and_argspect, but
        # cononical_parts_from_method already does that.
        method = parts['action']
        if parts['prefix']:
            method = '%s_%s' % (parts['prefix'], parts['action'])

        name_counters[route_name] = name_counters.get(route_name, 0) + 1
        if name_counters[route_name] > 1:
            route_name = '%s-%d' % (route_name, name_counters[route_name])

        tkwargs = dict(
            template=route_path,
            handler=controllercls,
            name=route_name,
            handler_method=method
        )

        tkwargs.update(kwargs)

        # ingest args[0] if its the only thing set
        if len(args) == 1:
            tkwargs['template'] = args[0]
        if len(args) > 1:
            raise ValueError("Only one positional argument may be passed to route_with")

        routes_list.append(Route(**tkwargs))

    return routes_list


def build_scaffold_routes_for_controller(controllercls, prefix_name=None):
    """
    Automatically sets up a restful routing interface for a controller
    that has any of the rest methods (list, view, add, edit, delete)
    either without or with a prefix. Note that these aren't true rest
    routes, some more wizardry has to be done for that.

    The routes generated are:

    controller:list : /controller
    controller:view : /controller/:id
    controller:add  : /controller/add
    controller:edit : /controller/:id/edit
    controller:delete : /controller/:id/delete

    prefixes just add to the beginning of the name and uri, for example:

    admin:controller:edit: /admin/controller/:id/edit
    """
    if(hasattr(controllercls, 'name')):
        name = controllercls.name
    name = inflector.underscore(controllercls.__name__)
    prefix_string = ''

    if prefix_name:
        prefix_string = prefix_name + '_'

    top = []
    path = []
    id = []

    # GET /controller -> controller::list
    if hasattr(controllercls, prefix_string + 'list'):
        top.append(Route('/' + name, controllercls, 'list', handler_method=prefix_string + 'list', methods=['HEAD', 'GET']))

    # GET /controller/:urlsafe -> controller::view
    if hasattr(controllercls, prefix_string + 'view'):
        path.append(Route('/:<key>', controllercls, 'view', handler_method=prefix_string + 'view', methods=['HEAD', 'GET']))

    # GET/POST /controller/add -> controller::add
    # POST /controller -> controller::add
    if hasattr(controllercls, prefix_string + 'add'):
        path.append(Route('/add', controllercls, 'add', handler_method=prefix_string + 'add', methods=['GET', 'POST']))
        top.append(Route('/' + name, controllercls, 'add:rest', handler_method=prefix_string + 'add', methods=['POST']))

    # GET/POST /controller/:urlsafe/edit -> controller::edit
    # PUT /controller/:urlsafe -> controller::edit
    if hasattr(controllercls, prefix_string + 'edit'):
        id.append(Route('/edit', controllercls, 'edit', handler_method=prefix_string + 'edit', methods=['GET', 'POST']))
        path.append(Route('/:<key>', controllercls, 'edit:rest', handler_method=prefix_string + 'edit', methods=['PUT', 'POST']))

    # GET /controller/:urlsafe/delete -> controller::delete
    # DELETE /controller/:urlsafe -> controller::d
    if hasattr(controllercls, prefix_string + 'delete'):
        id.append(Route('/delete', controllercls, 'delete', handler_method=prefix_string + 'delete'))
        path.append(Route('/:<key>', controllercls, 'delete:rest', handler_method=prefix_string + 'delete', methods=["DELETE"]))

    top_route = routes.NamePrefixRoute(name + ':', top + [
        routes.PathPrefixRoute('/' + name, path + [
            routes.PathPrefixRoute('/:<key>', id)
        ])
    ])

    if prefix_name:
        prefix_route = routes.NamePrefixRoute(prefix_name + ':', [
            routes.PathPrefixRoute('/' + prefix_name, [top_route])
        ])
        return prefix_route

    return top_route
