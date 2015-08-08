from ferris import plugins

plugins.register('angular', templating=False)

import ferris
import os
from ferris.core import template

template.add_template_path(
    os.path.normpath(os.path.join(
        os.path.dirname(ferris.__file__),
        '../angular-app/templates')),
    'angular')
