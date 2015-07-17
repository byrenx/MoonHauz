from ferris import Controller, route_with


class Angular(Controller):

    @route_with(template='/view/<name:.*>')
    def show(self, name):
        self.meta.view.template_name = 'angular/' + name

