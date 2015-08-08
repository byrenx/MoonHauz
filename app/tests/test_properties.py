from ferrisnose import FerrisAppTest

class TestProperties(FerrisAppTest):

    get = lambda self, url: self.testapp.get(url)
    delete = lambda self, url: self.testapp.delete(url)
    jget = lambda self, url: self.testapp.get(url).json
    jpost = lambda self, url, params: self.testapp.post_json(url, params).json

    login_email = 'test@example.com'

    def setUp(self):
        super(self.__class__, self).setUp()
        self.loginUser(email=self.login_email, admin=True)

    def testCRUD(self):
        #land
        params = {'name': 'Vista Land', 'location': 'Bacoor City, Cavite City',
                  'sold': False, 'price': 12201122,
                  'transaction_type': 1,
                  'features': 'located in the very accessible place in Bacoor,\
                  has pools and farm lands and with stores inside area. It was previously a housing community.'}
        resp = self.jpost('/api/property/create', params)

        assert resp['name'] == 'Vista Land'

        key = resp['key']['urlsafe']

        update_params = {'name': 'Agent Huntington'}
        resp = self.jpost('/api/property/update/:' + key, update_params)

        assert resp['name'] == 'Agent Huntington'

        #self.delete('/api/agents/:' + key)
