import logging
import ferris
import os

_plugins = []


def exists(name):
    """
    Checks to see if a particular plugin is enabled
    """
    return name in _plugins


def register(name, templating=True):
    """
    Adds a plugin's template path to the templating engine
    """
    import template
    _plugins.append(name)

    if templating:
        path = os.path.normpath(os.path.join(
            os.path.dirname(ferris.__file__),
            '../plugins/%s/templates' % name))
        template.add_template_path(path)
        template.add_template_path(path, prefix=name)


def enable(name):
    """
    Routes all of the controllers inside of a plugin
    """
    from routing import route_all_controllers
    try:
        route_all_controllers(ferris.app.app.router, name)
    except ImportError, e:
        logging.error("Plugin %s does not exist, or contains a bad import: %s" % (name, e))
        raise


def list():
    return _plugins
