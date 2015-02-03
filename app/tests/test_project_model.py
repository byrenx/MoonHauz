from ferrisnose import FerrisAppTest
from app.models.project import Project
import uuid

class TestProjectModel(FerrisAppTest):
    
    def setUp(self):
        super(self.__class__, self).setUp()
        project_params = {'name' : 'BeckTaxi', 'total_hours' : 100}
        self.project = Project.create(project_params)

    """ Test Create project """
    def testCreate(self):
        assert self.project.key.urlsafe
        assert self.project.name == 'BeckTaxi'
        assert self.project.total_hours == 100

    """ test Retrieve """
    def testRetrieve(self):
        data = Project.find_by_name(self.project.name)
        assert data.key == self.project.key
        assert data.name == self.project.name
        assert data.total_hours == self.project.total_hours
        
