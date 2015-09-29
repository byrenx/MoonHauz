from ferris import messages, route_with
from app.controllers.base_controller import MoonHauzController
from app.models.property import Property
from app.models.house_and_lot import HouseAndLot
from app.models.land import Land
from app.models.condo_unit import CondoUnit
from app.models.apartment import Apartment


class Debug(MoonHauzController):
    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging,)
        
    # @route_with("/api/import_mock_data", method=['GET']):
    # def import_csv(self):

    @route_with("/api/init_lands", methods=['GET'])
    def api_init_lands(self):
        pass
        
        

