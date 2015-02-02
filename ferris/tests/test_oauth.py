from ferrisnose import AppEngineTest
from google.appengine.api import users
from ferris.core.oauth2.user_credentials import UserCredentials, find_credentials


class TestOAuth(AppEngineTest):

    def test_credential_storage(self):
        user1 = users.User("test@example.com")
        user2 = users.User("test2@example.com")

        assert UserCredentials.query().count() == 0

        UserCredentials.create(
            user=user1,
            scopes=['a', 'c', 'b'],
            credentials=None,
            admin=False
        )

        UserCredentials.create(
            user=user2,
            scopes=['e', 'f', 'g'],
            credentials=None,
            admin=True
        )

        assert UserCredentials.query().count() == 2
        assert find_credentials(user=user1, scopes=['a', 'b', 'c']), "Should find out of order scopes credentials"
        assert find_credentials(user=user1, scopes=['a', 'c', 'b']), "Should find credentials"
        assert not find_credentials(user=user1, scopes=['a', 'b', 'd']), "Should not find credentials when scopes don't match"
        assert not find_credentials(user=user1, scopes=['a', 'b', 'c'], admin=True), "Should not find credentials that aren't admin"

        UserCredentials.create(
            user=user1,
            scopes=['a', 'c', 'b'],
            credentials=None,
            admin=False
        )

        assert UserCredentials.query().count() == 2, "Should overwrite existing credentials"

        assert find_credentials(scopes=['e', 'g', 'f'], admin=True), "Should find admin scopes"
