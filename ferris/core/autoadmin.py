"""
Provides automatic registration of admin controllers to the admin nav bar
"""

import webapp2
from ferris.core import events, inflector, controller


@events.on('before_template_render')
def render_template_listener(name, context, env):

    admin_links = {}
    for x in controller.Controller._controllers:
        try:
            admin_links[x.__name__] = webapp2.uri_for('admin:' + inflector.underscore(x.__name__) + ':list')
        except:
            pass

    context.update({
        'autoadmin': {
            'links': admin_links
        }
    })
