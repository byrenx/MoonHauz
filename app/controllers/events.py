from ferris import Controller, messages, route_with, route
from ferris.components.pagination import Pagination
from app.models.event import Event
from datetime import timedelta

import json
import datetime
import logging

class Events(Controller):

    class Meta:
        components = (messages.Messaging, Pagination,)
        Model = Event
        pagination_limit = 25
        prefixes = ('api',)

    @route_with('/api/events/list', methods=['GET'])
    def api_list(self):
        self.context['data'] = Event.list_all()

    @route_with('/api/events/find/:<key>', methods=['GET'])
    def api_find(self,key):
        id = self.util.decode_key(key)
        items = Event.find_by_allocation(id)
        self.context['data'] = items


    @route_with('/api/events/create', methods=['POST'])
    def api_create(self):
        params = json.loads(self.request.body)
        key = self.util.decode_key(params['allocation_id']['urlsafe'])

        for i in range (len(params['events'])):
            start = datetime.datetime.utcfromtimestamp(float(params['events'][i]['start_date'])) + datetime.timedelta(days=1)
            end = datetime.datetime.utcfromtimestamp(float(params['events'][i]['end_date'])) + datetime.timedelta(days=1)
            frequency = int(params['events'][i]['frequency'])
            total_hours = int(params['events'][i]['total'])
            data ={'allocation_id' : key, 'start_date' : start, 'frequency' : frequency, 'total_hours' : total_hours, 'end_date' : end}
            Event.create(data)

        return 200

    @route_with('/api/events/:<key>', methods=['DELETE'])
    def api_delete(self, key):
        items = self.util.decode_key(key).get()
        retHour = items.total_hours
        retID = items.project_id
        retData = Project.find_by_proj_key(retID)
        print retData
        Project.retHours(retData, retHour)
        items.delete()
        return 200
