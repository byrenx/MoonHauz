from ferris import BasicModel, ndb

class Task(BasicModel):
    taskContent = ndb.StringProperty()
    resource_name = ndb.StringProperty()
    project_name = ndb.StringProperty()
    event = ndb.StringProperty()

    @classmethod
    def list_all(cls):
        return cls.query().order(cls.resource_name)

    @classmethod
    def find_by_task_id(cls, task_id):
        return cls.query().filter(cls.key == task_id)

    @classmethod
    def get(cls, key):
        return cls(parent=key)

    @classmethod
    def update(self, params):
        self.populate(**params)
        self.put()

    @classmethod
    def updateTaskContent(self, key, params):
        data = self.query(self.key == key).fetch()
        print repr(data)
        data[0].taskContent=params['taskContent']
        data[0].put()


    @classmethod
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item
