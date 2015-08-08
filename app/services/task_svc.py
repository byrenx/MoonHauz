from app.models.task import Task
from app.models.user.selling_partner import SellingPartner
from app.services.user_svc import UserSvc
import datetime
from dateutil import relativedelta
import logging


class TaskSvc:

    @staticmethod
    def create_self_assessment_tasks_new_partners():

        def process(partners):
            for partner_key in partners:
                TaskSvc.create_self_assessment_task(partner_key)

        today = datetime.date.now()
        previous_dates = []
        previous_dates.append(today - relativedelta.relativedelta(months=3) - datetime.timedelta(days=30))
        previous_dates.append(today - relativedelta.relativedelta(months=8) - datetime.timedelta(days=30))
        previous_dates.append(today - relativedelta.relativedelta(months=9) - datetime.timedelta(days=30))
        previous_dates.append(today - relativedelta.relativedelta(months=12) - datetime.timedelta(days=30))
        for d in previous_dates:
            partners = SellingPartner.query(SellingPartner.date_joined == d).fetch(keys_only=True)
            process(partners)

    @staticmethod
    def create_self_assessment_tasks_old_partners():
        # TODO: fill in logic notes
        # Query all SP who joined 23 months ago and beyond
        # Create an SP task for each of those who are exactly 23 mos., 35 mos., 47 mos., ...
        # (for loop: get join date, subtract from today's date, subtract 11 mos, answer should be % 12 == 0)
        today = datetime.date.now()
        a23_months_ago = today - relativedelta.relativedelta(months=24) - datetime.timedelta(days=30)
        partners = SellingPartner.query(SellingPartner.date_joined >= a23_months_ago).fetch(keys_only=True)
        for partner_key in partners:
            partner = partner_key.get()
            # (today - partner.date_joined).days
            TaskSvc.create_self_assessment_task(partner_key)

    @staticmethod
    def create_self_assessment_task(selling_partner_key):
        selling_partner = selling_partner_key.get()
        params = {
            'branch': selling_partner.branch,
            'ops_group': selling_partner.ops_group,
            'section': selling_partner.section,
            'due_date': datetime.datetime.now() + datetime.timedelta(days=30),
        }
        Task(kind='SelfAssessment', selling_partner=selling_partner_key, due_date=due_date, **params).put()

    # TODO: to be hooked in self-assessment submission
    # RTM#25 Once a Selling Partner has completed a self assessment, a task is created for their section manager to review the self assessment. The task is due 30 days from the date of completion of the self assessment
    @staticmethod
    def create_review_task(self_assessment_key):
        self_assessment = self_assessment_key.get()
        selling_partner = self_assessment.selling_partner.get()
        params = {
            'branch': selling_partner.branch,
            'ops_group': selling_partner.ops_group,
            'section': selling_partner.section,
            'due_date': datetime.datetime.now() + datetime.timedelta(days=30),
        }
        Task(kind='Review', self_assessment=self_assessment_key, due_date=due_date, **params).put()

    @staticmethod
    def create_observation_task(selling_partner_key):
        selling_partner = selling_partner_key.get()
        params = {
            'branch': selling_partner.branch,
            'ops_group': selling_partner.ops_group,
            'section': selling_partner.section,
            'due_date': datetime.datetime.now() + datetime.timedelta(days=30),
        }
        Task(kind='Observation', selling_partner=selling_partner_key, due_date=due_date, **params).put()

    # TODO: to be hooked in self-assessment submission
    # RTM#26 If the self assessment was linked to a task, the task is marked as complete once the self assessment is submitted
    @staticmethod
    def self_assessment_done():
        me = UserSvc.get_current_user(key_only=True)
        Task.mark_as_complete_by_user('SelfAssessment', me)

    # TODO: to be hooked in review submission
    # RTM#31 If the review was linked to one or more tasks, the tasks are marked as complete once the review is submitted. Note that a review may be linked to tasks for both the Selling Coach and Section Manager.
    @staticmethod
    def review_done(assessment_key):
        Task.mark_as_complete_by_assessment('Review', assessment_key)

    # TODO: to be hooked in observation submission
    # RTM#37 If the observation was linked to a task, the task is marked as complete once the observation is submitted
    @staticmethod
    def observation_done(selling_partner_key):
        Task.mark_as_complete_by_user('Observation', selling_partner_key)

    @staticmethod
    def get_my_tasks():
        me = UserSvc.get_current_user()
        if 'Manager' in me._class_name():
            pass
        return Task.get_all_user_tasks(me)

    # TODO: implement!
    # RTM#53 Any tasks for any user that relate to the Selling Partner are deleted at that time as well.
    @staticmethod
    def delete_tasks(selling_partner_key):
        pass
