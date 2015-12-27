from ferris import messages, route_with
from app.controllers.base_controller import MoonHauzController
from ferris.components.pagination import Pagination
from app.models.property import Property
from app.models.house_and_lot import HouseAndLot
from app.models.land import Land
from app.models.condo_unit import CondoUnit
from app.services.utils import gather_keys, json_loads
from app.lib import cloudstorage as gcs


class Properties(MoonHauzController):
    class Meta:
        prefixes = ('api',)
        components = (messages.Messaging, Pagination,)
        Model = Property
        Message = Property.message()
        pagination_limit = 8
        keys = gather_keys(Model)

    @route_with("/api/properties", methods=['GET'])
    def api_list_all(self):
        self.context['data'] = self.components.pagination.paginate(query=Property.query(), limit=self.Meta.pagination_limit)

    @route_with("/api/property/:<key>", methods=['GET'])
    def api_get_property(self, key):
        """
        (Properties, key) --> Property Message
        
        Return a Property Message based from urlsafe key
        """
        prop = self.util.decode_key(key).get()
        self.context['data'] = Property.to_message(prop)

    @route_with("/api/property/land/create", methods=['POST'])
    def api_create_land(self):
        self.meta.Model = Land
        land = Land.create(json_loads(self.request.body, self.meta.keys))
        self.meta.Message = messages.model_message(Land)
        self.context['data'] = land

    @route_with("/api/property/house_and_lot/create", methods=['POST'])
    def api_create_house_and_lot(self):
        self.meta.Model = HouseAndLot
        h_and_l = HouseAndLot.create(json_loads(self.request.body, self.meta.keys))
        self.context['data'] = h_and_l

    @route_with("/api/property/condo_unit/create", methods=['POST'])
    def api_create_condo_unit(self):
        self.meta.Model = CondoUnit
        condo_unit = CondoUnit.create(json_loads(self.request.body, self.meta.keys))
        self.context['data'] = condo_unit

    '''
    update properties
    '''
    @route_with("/api/property/land/update/:<p_key>", methods=['POST'])
    def api_update_land(self, p_key):
        self.meta.Model = Land
        land = self.util.decode_key(p_key).get()
        land.update(json_loads(self.request.body, self.meta.keys))
        self.meta.Message = messages.model_message(Land)
        self.context['data'] = land

    @route_with("/api/property/house_and_lot/update/:<p_key>", methods=['POST'])
    def api_update_house_and_lot(self, p_key):
        self.meta.Model = HouseAndLot
        h_and_l = self.util.decode_key(p_key).get()
        h_and_l.update(json_loads(self.request.body, self.meta.keys))
        self.context['data'] = h_and_l

    @route_with("/api/property/condo_unit/update/:<p_key>", methods=['POST'])
    def api_update_condo_unit(self, p_key):
        self.meta.Model = CondoUnit
        condo_unit = self.util.decode_key(p_key).get()
        condo_unit.update(json_loads(self.request.body, self.meta.keys))
        self.context['data'] = condo_unit

    @route_with("/api/property/search_by_location/:<location>")
    def api_search_by_location(self, location):
        properties = self.components.pagination.paginate(query=Property.list_by_location(location), limit=6)
        self.context['data'] = properties

    @route_with("/api/upload_photo")
    def api_upload_photo(self):
        """
        upload photo to cloud storage and
        mutate the photo_urls list of the Property entity
        identified by property_key
        """
        input_file = self.request.params['file']
        p_key = self.request.params['property_key']

        gcs_filepath = "/moonhauz/images/%s" % input_file.filename
        with gcs.open(gcs_filepath, 'w') as f:
            try:
                line = input_file.file.readline()
                while line:
                    f.write(line)
                    line = input_file.file.readline()
                # Get Property entity
                self.Meta.Model = Land
                prop = self.util.decode_key(p_key).get()
                # mutate Property photo urls list
                prop.images_urls = prop.images_urls + [gcs_filepath]
                prop.put()
                return 200
            except:
                return 404
