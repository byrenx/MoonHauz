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
        pagination_limit = 8
        keys = gather_keys(Model)

    @route_with("/api/apartments", methods=['GET'])
    def api_list_all(self):
        self.context['data'] = self.components.pagination.paginate(query=Apartment.query(), limit=self.Meta.pagination_limit)


