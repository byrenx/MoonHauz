from ferris import messages, Controller, route_with
from app.controllers.base_controller import MoonHauzController
from app.models.property import Property
from app.models.house_and_lot import HouseAndLot
from app.models.land import Land
from app.models.condo_unit import CondoUnit
from app.models.apartment import Apartment


class Debug(Controller):
    # class Meta:
    #     prefixes = ('api',)
    #     components = (messages.Messaging,)
    
    # @route_with("/api/import_mock_data", method=['GET']):
    # def import_csv(self):

    @route_with("/api/init_lands", methods=['GET'])
    def api_init_lands(self):
        for i in range(30):
            Land.create({'name':"Land Prop Sample",
                         'location':"Manila Philippines",
                         'price':10000,
                         'transaction_type':"SALE",
                         'features':"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                         'geo_point': "14.581423745728499, 120.98453521728517",
                         'land_type':"INDUSTRIAL",
                         'land_area':3000})
        return 200

    @route_with("/api/init_house_and_lot", methods=['GET'])
    def api_init_house_and_lot(self):
        for i in range(30):
            HouseAndLot.create({'name':"House And Lot Prop Sample",
                                'location':"Manila Philippines",
                                'floors': 3,
                                'bedrooms': 4,
                                'floor_area': 2302,
                                'price':10000,
                                'transaction_type':"SALE",
                                'features':"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                                'geo_point': "14.581423745728499, 120.98453521728517",
                                'land_area':3000})
        return 200


    @route_with("/api/init_condo_unit", methods=['GET'])
    def api_init_condo_unit(self):
        for i in range(30):
            CondoUnit.create({'name':"Condo Unit Prop Sample",
                              'location':"Manila Philippines",
                              'capacity': 4,
                              'bedrooms': 4,
                              'floor_area': 2302,
                              'price':10000,
                              'transaction_type':"RENT",
                              'features':"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                              'geo_point': "14.581423745728499, 120.98453521728517"})
        return 200

    @route_with("/api/init_apartment", methods=['GET'])
    def api_init_condo_unit(self):
        for i in range(30):
            Apartment.create({'name':"Apartment Prop Sample",
                              'location':"Manila Philippines",
                              'bedrooms': 4,
                              'floor_area': 2302,
                              'price':10000,
                              'transaction_type':"RENT",
                              'features':"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
                              'geo_point': "14.581423745728499, 120.98453521728517"})
        return 200


    @route_with('/api/delete_all_props', methods=['GET'])
    def api_delete_all(self):
        for e in Property.query().iter(keys_only=True):
            e.delete()
        return 200
    
        
        

