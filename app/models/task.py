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
    def create(cls, params):
        item = cls()
        item.populate(**params)
        item.put()
        return item
