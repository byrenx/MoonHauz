from ferris import Controller, route_with, messages
#from app.misc.auth import only
from google.appengine.api import users
from protorpc import protojson


class Main(Controller):

    @route_with(template='/')
    def index(self):
        self.meta.view.template_name = 'angular/app-index.html'
 
    @route_with(template='/admin')
    def admin(self):
        user = users.get_current_user()
        if user:
            self.context['logout_url'] = users.create_logout_url('/')
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.meta.view.template_name = 'angular/admin-index.html'
        

