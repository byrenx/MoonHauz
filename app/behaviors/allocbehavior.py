from ferris.core.ndb import Behavior
from app.models.project import Project

class AllocBehavior(Behavior):

    def __init__(self, Model):
        self.Model = Project

    def after_delete(self, key):
        #print repr(key)
        pass
