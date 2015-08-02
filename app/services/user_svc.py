from google.appengine.api import users
from app.models.assessment import Assessment
from app.models.user.user import User
# roles
from app.models.user.branch_manager import BranchManager
from app.models.user.customer_experience_team import CustomerExperienceTeam
from app.models.user.ops_manager import OpsManager
from app.models.user.section_manager import SectionManager
from app.models.user.selling_coach import SellingCoach
from app.models.user.selling_partner import SellingPartner
import logging


class UserSvc:

    @staticmethod
    def create_selling_partner():
        user = users.get_current_user()
        return SellingPartner.create(email=user.email())

    @staticmethod
    def get_current_user(key_only=False):
        user = users.get_current_user()
        return User.get(user.email(), key_only=key_only)

    @staticmethod
    def move_section(user, section_key):
        section = section_key.get()
        user.branch = section.branch
        user.ops_group = section.ops_group
        user.section = section_key
        incomplete = Assessment.query(Assessment.selling_partner == user.key, Assessment.submitted == False)
        map(lambda a: a.move_section(section_key), incomplete)

    @staticmethod
    def generate_logout_url():
        return users.create_logout_url('/')
