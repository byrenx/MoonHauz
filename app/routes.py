from ferris.core import routing, plugins

# Routes all App handlers
routing.auto_route()

# Default root route
routing.default_root()


# Plugins
plugins.enable('angular')
#plugins.enable('settings')
#plugins.enable('oauth_manager')
