from ferris.core import plugins
import threading
import logging
from .models.setting import Setting as SettingsModel
from ferris import events
from google.appengine.api import memcache
import datetime


plugins.register('settings')

global_cache = {}
local_cache = threading.local()


def activate(settings):
    if 'overrides' not in global_cache:
        global_cache['overrides'] = SettingsModel.get_settings(settings)
    settings.update(global_cache['overrides'])
    global_cache['cts'] = datetime.datetime.utcnow()


def is_active():
    return 'overrides' in global_cache


def clear_global_cache():
    if is_active():
        del global_cache['overrides']


@events.on('after_settings')
def check_update_settings(settings):
    if hasattr(local_cache, 'checked'):
        activate(settings)
        return

    local_cache.checked = True

    cts = global_cache.get('cts', None)
    nts = memcache.get('_ferris_settings_update_mutex')
    if (nts and cts and nts > cts) or (nts and not cts):
        logging.info("Settings update detected. Reloading.")
        clear_global_cache()
    global_cache['cts'] = nts

    activate(settings)
