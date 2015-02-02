from __future__ import absolute_import
from google.appengine.ext import ndb
from ferris.core.controller import Controller, route, route_with
from oauth2client.client import OAuth2WebServerFlow
from ferris.core.oauth2.user_credentials import UserCredentials as OAuth2UserCredentials
from ferris.core import settings


class Oauth(Controller):

    @route
    def start(self, session):
        config = settings.get('oauth2')

        session = ndb.Key(urlsafe=session).get()
        callback_uri = self.uri(action='callback', _full=True)

        flow = OAuth2WebServerFlow(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            scope=session.scopes,
            redirect_uri=callback_uri)

        flow.params['state'] = session.key.urlsafe()

        if session.admin or session.force_prompt:
            flow.params['approval_prompt'] = 'force'

        uri = flow.step1_get_authorize_url()

        session.flow = flow
        session.put()

        return self.redirect(uri)

    @route_with(template='/oauth2callback')
    def callback(self):
        session = ndb.Key(urlsafe=self.request.params['state']).get()

        credentials = session.flow.step2_exchange(self.request.params['code'])

        OAuth2UserCredentials.create(
            user=self.user,
            scopes=session.scopes,
            credentials=credentials,
            admin=session.admin
        )

        session.key.delete()  # No need for the session any longer

        return self.redirect(str(session.redirect))
