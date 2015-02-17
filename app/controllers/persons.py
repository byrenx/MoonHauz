from ferris import Controller, messages, route_with
from ferris.components.pagination import Pagination
from app.models.person import Person
import json


class Persons(Controller):

    class Meta:
        components = (messages.Messaging, Pagination,)
        Model = Person
        pagination_limit = 25
        prefixes = ('api',)

    @route_with('/api/persons/list', methods=['GET'])
    def api_list(self):
        self.context['data'] = self.components.pagination.paginate(query=Person.list_all())

    @route_with('/api/persons/create', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        self.context['data'] = Person.create(params)

    @route_with('/api/persons/:<key>', methods=['GET'])
    def api_get(self, key):
        person = self.util.decode_key(key).get()
        self.context['data'] = person

    @route_with('/api/persons/:<key>', methods=['POST'])
    def api_update(self, key):
        params = json.loads(self.request.body)
        person = self.util.decode_key(key).get()
        person.update(params)
        self.context['data'] = person

    @route_with('/api/persons/:<key>', methods=['DELETE'])
    def api_delete(self, key):
        person = self.util.decode_key(key).get()
        person.delete()
        return 200


