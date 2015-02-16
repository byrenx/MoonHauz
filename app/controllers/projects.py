from ferris import Controller, messages, route_with
from ferris.components.pagination import Pagination
from app.models.project import Project
import json


class Projects(Controller):

    class Meta:
        components = (messages.Messaging, Pagination,)
        Model = Project
        pagination_limit = 25
        prefixes = ('api',)

    @route_with('/api/projects/list', methods=['GET'])
    def api_list(self):
        self.context['data'] = self.components.pagination.paginate(query=Project.list_all())

    @route_with('/api/projects/create', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        hours = int(params['billable_hours']);
        params['billable_hours'] = hours
        params['remaining_hours'] = hours
        self.context['data'] = Project.create(params)

    @route_with('/api/projects/:<key>', methods=['GET'])
    def api_get(self, key):
        project = self.util.decode_key(key).get()
        self.context['data'] = project

    @route_with('/api/projects/:<key>', methods=['POST'])
    def api_update(self, key):
        params = json.loads(self.request.body)
        keyS = self.util.decode_key(params['key']['urlsafe'])
        Project.updateHours(params,keyS)

    @route_with('/api/projects/:<key>', methods=['DELETE'])
    def api_delete(self, key):
        project = self.util.decode_key(key).get()
        project.delete()
        return 200


