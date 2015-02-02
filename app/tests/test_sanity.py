from ferrisnose import FerrisAppTest


class SanityTest(FerrisAppTest):

    def testRoot(self):
        self.loginUser()
        resp = self.testapp.get('/')

        self.loginUser(admin=True)
        resp = self.testapp.get('/admin')
        self.assertTrue('Ferris' in resp)
