from ferrisnose import AppEngineTest, FerrisAppTest, AppEngineWebTest

import logging
logging.warning("Ferris test lib is deprecated. Please use the new utilties provided by FerrisNose")


class WithTestBed(AppEngineTest):
    pass


class AppTestCase(FerrisAppTest):
    pass


class FerrisTestCase(AppEngineWebTest):
    pass
