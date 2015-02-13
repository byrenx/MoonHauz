from ferrisnose import FerrisAppTest
from app.models.allocation import Allocation
from app.models.person import Person
from app.models.project import Project
from datetime import timedelta
import datetime
import uuid


class TestAllocation(FerrisAppTest):
    
    def setUp(self):
        super(self.__class__, self).setUp()
        ''' create person to be the resource '''
        person_params = {'name' : 'John', 'color' : 'Parrot'}
        self.person = Person.create(person_params)

        ''' create project instance'''
        project_params = {'name' : 'BeckTaxi', 'billable_hours' : 100, 'start_date' : '1/28/2015'}
        project_params['start_date'] = datetime.datetime.strptime(project_params['start_date'], '%m/%d/%Y')
        self.project = Project.create(project_params)
        ''' create allocation instance '''
        # params = {'date_from': '1/28/2015', 'date_to': '1/29/2015'}
        # params['date_from'] = datetime.datetime.strptime(params['date_from'], '%m/%d/%Y')
        alloc_params = {
            'project_id' : self.project.key,
            'person_id' : self.person.key,
            
            'hours' : 20
        }


        self.allocation = Allocation.create(alloc_params)
        
    ''' Test Create Allocation '''
    def testCreate(self):
        assert self.allocation.project_id == self.project.key
        assert self.allocation.person_id == self.person.key
        assert self.allocation.start_date
        assert self.allocation.alloc_hours == 20
