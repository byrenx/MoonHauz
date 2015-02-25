from ferris.core.ndb import Behavior
from app.models.project import Project

class AllocBehavior(Behavior):

    def __init__(self, Model):
        self.Model = (Project,)

    def after_delete(self, key):
        pass

    def after_put(self, instance):
        total_hours = instance.temp_alloc
        if instance.temp_type == 'minus':
            pass
        else:
            proj_params = Project.find_by_proj_key(instance.project_id)
            rem_hours = Project.removeHours(proj_params, total_hours)
            return rem_hours


