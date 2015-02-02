from ferrisnose import AppEngineTest
from ferris.core.bunch import Bunch


class TestBunch(AppEngineTest):

    def test_bunch(self):
        data = Bunch()

        # test __getitem__
        data.entry = 'test'
        assert data.__getitem__('entry') == 'test'

        # test __setitem__
        data.__setitem__('entry', 'changed')
        assert data.entry == 'changed'

        # test __iter__
        for x in data:
            assert x == 'entry'

        # TODO: test __unicode__
        # --- following line gives:
        #     AttributeError: 'dict' object has no attribute '__unicode__'
        # data.__unicode__()

        # test __str__
        data.__str__()
