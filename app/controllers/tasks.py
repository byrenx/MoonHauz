from ferris import Controller, messages, route_with
from ferris.components.pagination import Pagination
from app.models.task import Task
import json

class Tasks(Controller):

   class Meta:
      components = (messages.Messaging, Pagination,)
      Model = Task
      pagination_limit = 25
      prefixes = ('api',)

   @route_with('/api/tasks/list', methods=['GET'])
   def api_list(self):
      self.context['data'] = self.components.pagination.paginate(query=Task.list_all())

   @route_with('/api/tasks/create', methods=['POST'])
   def api_create(self):
      params = json.loads(self.request.body)
      self.context['data'] = Task.create(params)

   @route_with('/api/tasks/:<key>', methods=['GET'])
   def api_get(self, key):
      task = self.util.decode_key(key).get()
      self.context['data'] = task

   @route_with('/api/tasks/:<key>', methods=['POST'])
   def api_update(self, key):
      params = json.loads(self.request.body)
      keyS = self.util.decode_key(key)
      Task.updateTaskContent(keyS, params)
      return 200

   @route_with('/api/tasks/:<key>', methods=['DELETE'])
   def api_delete(self, key):
      task = self.util.decode_key(key).get()
      task.delete()
      return 200

