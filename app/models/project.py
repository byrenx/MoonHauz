from ferris import BasicModel, ndb

class Project(BasicModel):
    name = ndb.StringProperty()
    total_hours = ndb.IntegerProperty()

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.name)
    
    @classmethod
    def find_by_project_id(cls, project_id):
        return cls.query().filter(cls.key == project_id)
    
    @classmethod
    def update(self, params):
        self.populate(**params)
        self.put()

    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item
    
