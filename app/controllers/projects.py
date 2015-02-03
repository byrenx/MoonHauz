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
        
    @route_with('/api/projects', methods=['GET'])
    def api_list(self):
        self.context['data'] = self.components.pagination.paginate(query=Project.list_all())
    
    @route_with('/api/projects', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        self.context['data'] = Project.create(params)

    @route_with('/api/projects/:<key>', methods=['GET'])
    def api_get(self, key):
        project = self.util.decode_key(key).get()
        self.context['data'] = project
    
    @route_with('/api/projects/:<key>', methods=['POST'])
    def api_update(self, key):
        params = json.loads(self.request.body)
        project = self.util.decode_key(key).get()
        project.update(params)
        self.context['data'] = project

    @route_with('/api/projects/:<key>', methods=['DELETE'])
    def api_delete(self, key):
        project = self.util.decode_key(key).get()
        project.delete()
        return 200


