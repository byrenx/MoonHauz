from ferris import Controller, messages, route_with, route
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
    project = Project()

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

    @route_with('/api/allocations/:<key>', methods=['GET'])
    def api_get(self, key):
        keyS = self.util.decode_key(key)
        items =  Allocation.find_by_project(keyS)
        self.context['data'] = items

    def isWeekend(self, myDate):
        return True if myDate.weekday() == 5 or myDate.weekday() == 6 else False

    @route_with('/api/allocations/calendar', methods=['GET'])
    def api_calendar(self):
        allocations = Allocation.list_all()
        events = []
        for items in allocations:
            total = items.alloc_hours
            divider = 8
            myDate = items.alloc_date
            while total > 0:
                if self.isWeekend(myDate) is False:
                    conv_date = myDate.strftime('%Y-%m-%d')
                    if total < 8:
                        events += [{'resource_name' : items.resource_name, 'color' : items.color, 'project_name' : items.project_name, 'alloc_date' : myDate.strftime('%Y-%m-%d'), 'alloc_hours' : total}]
                    else:
                        events += [{'resource_name' : items.resource_name, 'color' : items.color, 'project_name' : items.project_name, 'alloc_date' : myDate.strftime('%Y-%m-%d'), 'alloc_hours' : 8}]
                    total -= 8
                myDate += datetime.timedelta(days=1)
        return json.dumps(events)


    @route_with('/api/allocations/create', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        key = self.util.decode_key(params['project_id']['urlsafe'])
        name = params['name']

        for i in range (len(params['resource_name'])):
            per = self.person.find_by_name(params['resource_name'][i]);
            alloc = datetime.datetime.utcfromtimestamp(float(params['alloc_date'][i])) + datetime.timedelta(days=1)
            alloc_hours = int(params['alloc_hours'][i])
            info = {'project_id' : key,
                    'alloc_hours' : alloc_hours,
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
    @route_with('/api/allocations/:<key>', methods=['DELETE'])
    def api_delete(self, key):
        items = self.util.decode_key(key).get()
        retHour = items.alloc_hours
        retID = items.project_id
        #print retID
        retData = Project.find_by_proj_key(retID)
        print retData
        Project.retHours(retData, retHour)
        #items.delete()
        return 200
       # self.context['data'] = Allocation.create(params)

