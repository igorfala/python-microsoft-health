try:
    from urllib.parse import urlencode
except ImportError:
    # Python 2.x
    from urllib import urlencode

from requests_oauthlib import OAuth2, OAuth2Session
from MicrosoftHealth.Exceptions import *
import datetime, json, requests

class MHOauth2Client(object):
    API_ENDPOINT = "https://api.microsofthealth.net"
    AUTHORIZE_ENDPOINT = "https://login.live.com/oauth20_authorize.srf?"
    TOKEN_ENDPOINT = 'https://login.live.com/oauth20_token.srf?'
    API_VERSION = 'v1'
    def __init__(self, client_id, client_secret, scope = None,
                 access_token=None, refresh_token=None,
                 *args, **kwargs):
        """
        Create a UAOauth2Client object. Specify the first 7 parameters if
        you have them to access user data. Specify just the first 2 parameters
        to start the setup for user authorization (as an example see gather_key_oauth2.py)
            - client_id, client_secret are in the app configuration page
            https://apps.dev.microsoft.com/?mkt=en-us#/application/cffef512-3b2f-4637-be70-f9da64e4896b
            - access_token, refresh_token are obtained after the user grants permission
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        self.oauth = OAuth2Session(client_id)
        self.scope = scope

    def make_request(self, url, data={}, method=None, **kwargs):
        """
        Builds and makes the OAuth2 Request, catches errors
        """
        if not method:
            method = 'post' if data else 'get'
        headers = {"Authorization": "bearer {0}".format(self.token.get('access_token'))}
        try:
            if method == 'get':
                response = getattr(requests, method)(url=url, headers=headers)
            else:
                response = getattr(requests, method)(url=url, headers=headers, data=data)
        except HTTPUnauthorized as e:
            # Check if needs_refresh in response,
            #then refresh token from outside and try again.
            response = {'needs_refresh': 'Please refresh the token'}

        if response.status_code == 401:
            raise HTTPUnauthorized(response.json())
        elif response.status_code == 403:
            raise HTTPForbidden(response.json())
        elif response.status_code == 404:
            raise HTTPNotFound(response.json())
        elif response.status_code == 405:
            raise HTTPMethodNotAllowed(response.json())
        elif response.status_code >= 500:
            raise HTTPServerError(response.json())
        return response.json()

    def authorize_token_url(self, redirect_uri=None, **kwargs):
        """Step 1: Return the URL the user needs to go to in order to grant us
        authorization to look at their data.  Then redirect the user to that
        URL, open their browser to it, or tell them to copy the URL into their
        browser.
            - scope: pemissions that that are being requested [default ask all]
            - redirect_uri: url to which the reponse will posted
                            required only if your app does not have one
            for more info see https://developer.microsoftband.com/Content/docs/MS%20Health%20API%20Getting%20Started.pdf
        """

        params = {"scope": self.scope,
                  "redirect_uri": redirect_uri}

        authorization_url = "%s%s" % (self.AUTHORIZE_ENDPOINT, urlencode(params))

        out = self.oauth.authorization_url(authorization_url)
        return(out)

    def fetch_access_token(self, code, redirect_uri):

        """Step 2: Given the code from Microsoft Health from step 1, call
        it again and returns an access token object. Extract the needed
        information from that and save it to use in future API calls.
        the token is internally saved
        """
        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        post_data = { "code": code,
                      "redirect_uri": redirect_uri,
                      "grant_type": "authorization_code"}
        response = requests.post(self.TOKEN_ENDPOINT,
                             auth=client_auth,
                             data=post_data)
        token_json = response.json()
        return token_json

    def refresh_token(self):
        """Step 3: obtains a new access_token from the the refresh token
        obtained in step 2.
        the token is internally saved
        """
        client_auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        post_data = { "refresh_token": self.token.get('refresh_token'),
                      "redirect_uri": redirect_uri,
                      "grant_type": "refresh_token"}
        response = requests.post(self.TOKEN_ENDPOINT,
                             auth=client_auth,
                             data=post_data)
        token_json = response.json()
        return token_json

class MH(object):
    US = 'en_US'
    METRIC = 'en_UK'

    API_ENDPOINT = "https://api.microsofthealth.net"
    API_VERSION = 1
    def __init__(self, microsoft_health_key, microsoft_health_secret, scope=None, system=US, access_token = None, **kwargs):
        """
        MH(<id>, <secret>, access_token=<token>, refresh_token=<token>)
        """
        self.system = system
        self.client = MicrosoftOauth2Client(microsoft_health_key, microsoft_health_secret,scope=scope, access_token=access_token)
        self.scope = scope
        # All of these use the same patterns, define the method for accessing
        # creating and deleting records once, and use curry to make individual
        # Methods for each

    def make_request(self, url, *args, **kwargs):
        # This should handle data level errors, improper requests, and bad
        # serialization
        response = self.client.make_request(url, data, method, *args, **kwargs)
        return response

    def user_profile_get(self, user_id=None):
        """
        Get a user profile. You can get other user's profile information
        by passing user_id, or you can get the current user's by not passing
        a user_id
        .. note:
            This is not the same format that the GET comes back in, GET requests
            are wrapped in {'user': <dict of user data>}
        """
        url = self.API_ENDPOINT + '/V1/me/profile'
        return self.make_request(url)
