from ferris import BasicModel, ndb

class Person(BasicModel):
    person_id = ndb.KeyProperty()
    firstname = ndb.StringProperty()
    lastname = ndb.IntegerProperty()
    
    @classmethod
    def list_all(cls):
        return cls.query().order(cls.lastname)
    
    @classmethod
    def find_by_person_id(cls, person_id):
        return cls.query().filter(cls.person_id == person_id)

    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item
    
    
    
    
