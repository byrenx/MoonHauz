from ferris import Controller, route_with, messages
#from app.misc.auth import only
from protorpc import protojson


class Main(Controller):

    @route_with(template='/')
    def index(self):
        self.meta.view.template_name = 'angular/app-index.html'
 
    @route_with(template='/admin')
    def admin(self):
        self.meta.view.template_name = 'angular/admin-index.html'
