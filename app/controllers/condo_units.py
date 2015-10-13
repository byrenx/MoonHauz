from ferris import messages, route_with
from app.controllers.base_controller import MoonHauzController
from ferris.components.pagination import Pagination
from app.models.condo_unit import CondoUnit
from app.services.utils import gather_keys, json_loads
import json


class CondoUnits(MoonHauzController):

    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging, Pagination,)
        Model = CondoUnit
        pagination_limit = 8
        keys = gather_keys(Model)
        
    @route_with("/api/condo_units")
    def api_list_all(self):
        self.context['data'] = self.components.pagination.paginate(query=CondoUnit.query(), limit=self.Meta.pagination_limit)

