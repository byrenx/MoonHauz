from ferris import Controller, messages, route_with
from ferris.components.pagination import Pagination
from app.models.allocation import Allocation
from datetime import timedelta

import json
import datetime
import logging

class Allocations(Controller):
    
    class Meta:
        components = (messages.Messaging, Pagination,)
        Model = Allocation
        pagination_limit = 25
        prefixes = ('api',)
    
    @route_with('/')
    def index(self):
        pass

    @route_with('/api/allocations/list', methods=['GET'])
    def api_list(self):
        self.context['data'] = self.components.pagination.paginate(query=Allocation.list_all())
    
    @route_with('/api/allocations/create', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        key = self.util.decode_key(params['project_id']['urlsafe'])
        print key
        for i in range (len(params['resource_name'])):
            print params['alloc_hours'][i]
            print params['resource_name'][i]
            print params['alloc_date']
            info = { 'project_id' : key,
                     'resource_name' : params['resource_name'][i],
                     'alloc_hours' : int(params['alloc_hours'][i]),
                     'alloc_date' : datetime.datetime.utcfromtimestamp(float(params['alloc_date'][i]))
                    }
            Allocation.create(info)

        return 200
       # self.context['data'] = Allocation.create(params)
        
        
