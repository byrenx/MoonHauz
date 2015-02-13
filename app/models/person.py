from ferris import BasicModel, ndb

class Person(BasicModel):
    name = ndb.StringProperty()
    color = ndb.StringProperty()
    
    @classmethod
    def list_all(cls):
        return cls.query().order(cls.lastname)
    
    @classmethod
    def find_by_person_id(cls, person_id):
        return cls.query().filter(cls.key == person_id)

    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item
    
    
    
    
