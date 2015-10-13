from ferris import messages, route_with
from app.controllers.base_controller import MoonHauzController
from ferris.components.pagination import Pagination
from app.models.land import Land
from app.services.utils import gather_keys, json_loads
import json

class Lands(MoonHauzController):

    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging, Pagination,)
        Model = Land
        pagination_limit = 8
        keys = gather_keys(Model)

    @route_with("/api/lands", methods=['GET'])
    def api_list_all(self):
        self.context['data'] = self.components.pagination.paginate(query=Land.query(), limit=self.Meta.pagination_limit)


