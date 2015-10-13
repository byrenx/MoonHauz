from ferris import messages, route_with
from app.controllers.base_controller import MoonHauzController
from ferris.components.pagination import Pagination
from app.models.house_and_lot import HouseAndLot
from app.services.utils import gather_keys, json_loads
import json

class HouseAndLots(MoonHauzController):

    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging, Pagination,)
        Model = HouseAndLot
        pagination_limit = 8
        keys = gather_keys(Model)

    @route_with("/api/house_and_lots", methods=['GET'])
    def api_list_all(self):
        self.context['data'] = self.components.pagination.paginate(query=HouseAndLot.query(), limit=self.Meta.pagination_limit)
   

