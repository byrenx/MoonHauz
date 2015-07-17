from ferris import Controller, route_with, messages
# from app.misc.auth import only
# from app.models.user.selling_partner import SellingPartner
# from app.models.user.user import User
# from app.services.user_svc import UserSvc
from protorpc import protojson


class Main(Controller):

    @route_with(template='/')
    def index(self):
        # active_user = UserSvc.get_current_user()
        # if not active_user:
        #     active_user = UserSvc.create_selling_partner()

        # if active_user._class_name() == 'SellingPartner':
        #     self.meta.Message = SellingPartner.message()
        #     self.meta.messaging_transform_function = SellingPartner.transform_message
        # else:
        #     self.meta.Message = User.message()
        #     self.meta.messaging_transform_function = User.transform_message

        # user = messages.to_message(active_user, messages.model_message(User))
        self.meta.view.template_name = 'angular/app-index.html'



    # @only("=", "CustomerExperienceTeam")
    @route_with(template='/admin')
    def admin(self):
        self.meta.view.template_name = 'angular/admin-index.html'
