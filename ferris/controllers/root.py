from ferris.core.controller import Controller, users


class Root(Controller):

    def root(self):
        self.meta.view.template_name = 'index.html'

    def admin(self):
        if not users.is_current_user_admin():
            return 401
        self.meta.view.template_name = 'admin_index.html'

    def error(self, code):
        code = int(code)
        self.abort(code, 'Just a test')
