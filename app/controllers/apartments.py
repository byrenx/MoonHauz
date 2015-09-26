from ferris import messages, route_with
from app.controllers.base_controller import MoonHauzController
from ferris.components.pagination import Pagination
from app.models.apartment import Apartment
from app.services.utils import gather_keys, json_loads
import json

class Apartments(MoonHauzController):

    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging, Pagination,)
        Model = Apartment
        pagination_limit = 6
        keys = gather_keys(Model)

    @route_with("/api/apartments", methods=['GET'])
    def api_list_all(self):
        self.context['data'] = Apartment.list_all().fetch()

