from ferris.core import time_util, settings
from ferrisnose import AppEngineTest
import datetime


class TestTime(AppEngineTest):
    def test_localize(self):
        settings.defaults({'timezone': {
            'local': 'US/Eastern'
        }})

        now = datetime.datetime.now()
        localized = time_util.localize(now)

        assert localized.tzinfo
        assert str(localized.tzinfo) == str(time_util.local_tz())
