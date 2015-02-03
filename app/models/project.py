from ferris import BasicModel, ndb

class Project(BasicModel):
    project_id = ndb.KeyProperty(required=True)
    project_name = ndb.StringProperty()
    total_hours = IntegerProperty()

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.project_name)
    
    @classmethod
    def find_by_project_id(cls, project_id):
        return cls.query().filter(cls.project_id == project_id)
    
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
    
