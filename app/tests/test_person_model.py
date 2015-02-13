from ferrisnose import FerrisAppTest
from app.models.person import Person
import uuid

class TestPersonModel(FerrisAppTest):
    
    def setUp(self):
        super(self.__class__, self).setUp()
        person_params = {'name' : 'John', 'color' : 'wasad'}
        self.person = Person.create(person_params)
        
    """ Test Add Person """
    def testCreate(self):
        assert self.person.key
        assert self.person.name == 'John'
        assert self.person.color == 'wasad'

    """ test retrieve a person """
    def testRetrieve(self):
        p = Person.find_by_name('John')
        assert p.key == self.person.key
        assert p.name == self.person.name
        assert p.color == self.person.color
        
