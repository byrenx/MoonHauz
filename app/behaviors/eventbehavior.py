from ferris.core.ndb import Behavior
from app.models.allocation import Allocation

class EventBehavior(Behavior):

    def __init__(self, Model):
        self.Model = Allocation

    def after_delete(self, key):
        pass

    def after_put(self, instance):
        total_hours = instance.total_hours
        alloc_params =  Allocation.find_allocation(instance.allocation_id)
        reflect_hours = Allocation.minusRemaining(alloc_params, total_hours)
        print total_hours

