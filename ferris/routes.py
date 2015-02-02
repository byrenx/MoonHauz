from ferris.core import routing

from ferris.controllers.root import Root
from ferris.controllers.oauth import Oauth

routing.add(routing.Route('/admin', Root, handler_method='admin'))
routing.add(routing.Route('/error/<code>', Root, handler_method='error'))
routing.route_controller(Oauth)
