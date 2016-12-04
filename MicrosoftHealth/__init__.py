# -*- coding: utf-8 -*-
"""
Microsoft Health API Library
------------------
:license: MIT, see LICENSE for more details.
------------------
Usage
  from MicrosoftHealth import MHOauth2Client, MH
  mhOauthObject = MHOauth2Client(client_id = mh_key, client_secret = mh_secret)
client_id, and client_secret are provided by Microsoft Health when registering your application
------------------
  url, state = mhOauthObject.authorize_token_url(mh_callback_url)
Let the user open the url. Save the state to the database
call_back_url is the url that you set when registering your app.
The user will be redirected to it after giving the app access to
their account. Under Armour will do a get request to that url
with a code. The code is used to get the token.
------------------
  tokenInfo = mhOauthObject.fetch_access_token(code)

tokenInfo contains all the info needed (access token, refresh token, etc.)
When getting the token info from Under Armour, save it to the database for later use.
------------------
  mhObject = MH(client_id = mh_key, client_secret = mh_secret, access_token=access_token)
Call the mhObject methods to interact with with Under Armour API.
Example:

  profile = mhObject.user_profile_get(user_id=mh_user_id)
------------------
For any methods that are not included in the library:

  result = mhObject.make_request(url, method, data)

The methods and data format could be found at:
https://developer.microsoftband.com/Content/docs/MS%20Health%20API%20Getting%20Started.pdf

"""
from .Exceptions import *
from .UnderArmour import MH, MHOauth2Client
# Meta info
__version__ = "0.1.0"
__author__ = "Igor Fala"
__license__ = 'MIT'
