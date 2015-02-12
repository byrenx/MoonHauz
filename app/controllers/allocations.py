from ferris import Controller, messages, route_with
from ferris.components.pagination import Pagination
from app.models.allocation import Allocation
from app.models.project import Project
from app.models.person import Person
from datetime import timedelta

import json
import datetime
import logging

class Allocations(Controller):
    person = Person()

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
        self.context['data'] = Allocation.list_all()

    @route_with('/api/allocations/calendar', methods=['GET'])
    def api_calendar(self):
        allocations = Allocation.list_all()
        self.context['data'] =  allocations

    @route_with('/api/allocations/create', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        key = self.util.decode_key(params['project_id']['urlsafe'])
        name = params['name']

        for i in range (len(params['resource_name'])):
            per = self.person.find_by_name(params['resource_name'][i]);
            alloc = datetime.datetime.utcfromtimestamp(float(params['alloc_date'][i])) + datetime.timedelta(days=1)
            info = {'project_id' : key,
                    'alloc_hours' : int(params['alloc_hours'][i]),
                    'project_name' : name,
                    'alloc_date' : alloc
                    }
            if per is not None:
                info['resource_name'] = per.name
                info['color'] = per.color
            else:
                person_params = {'name' : params['resource_name'][i], 'color' : params['color'][i]}
                self.person.create(person_params)
                info['resource_name'] = params['resource_name'][i]
                info['color'] = params['color'][i]
            Allocation.create(info)

        return 200
       # self.context['data'] = Allocation.create(params)


