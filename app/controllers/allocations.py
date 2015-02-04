from ferris import Controller, messages, route_with
from ferris.components.pagination import Pagination
from app.models.allocation import Allocation
from datetime import timedelta

import json
import datetime

class Allocations(Controller):
    
    class Meta:
        components = (messages.Messaging, Pagination,)
        Model = Allocation
        pagination_limit = 25
        prefixes = ('api',)
    
    @route_with('/')
    def index(self):
        pass

    @route_with('/api/allocations', methods=['GET'])
    def api_list(self):
        self.context['data'] = self.components.pagination.paginate(query=Allocation.list_all())
    
    @route_with('/api/allocationss', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        params['hours']
        self.context['data'] = Allocation.create(params)
        
        
