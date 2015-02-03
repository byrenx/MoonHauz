from ferrisnose import FerrisAppTest
from app.models.person import Person
import uuid

class TestPersonModel(FerrisAppTest):
    
    def setUp(self):
        super(self.__class__, self).setUp()
        person_params = {'firstname' : 'John', 'lastname' : 'Parrot'}
        self.person = Person.create(person_params)
        
    """ Test Add Person """
    def testCreate(self):
        assert self.person.key
        assert self.person.firstname == 'John'
        assert self.person.lastname == 'Parrot'

    """ test retrieve a person """
    def testRetrieve(self):
        p = Person.find_by_firstname('John')
        assert p.key == self.person.key
        assert p.firstname == self.person.firstname
        assert p.lastname == self.person.lastname
        
