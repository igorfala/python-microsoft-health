Python Microsoft Health SDK
=======================
Python library that can be used to connect and interact with Microsoft Health API.

----

**Installation**

Python2:
::
  pip install MSHealth
Python3:
::
  pip3 install MSHealth

----

**Requirements**

* Python 2.7+
* `requests-oauthlib`_ (to authenticate)
* `requests`_ (to make requests)

.. _requests-oauthlib: https://pypi.python.org/pypi/requests-oauthlib
.. _requests: https://pypi.python.org/pypi/requests

----

**Usage**
::
  from MicrosoftHealth import MHOauth2Client, MH
  mhOauthObject = MHOauth2Client(client_id = mh_key, client_secret = mh_secret)
client_id, and client_secret are provided by Under Armour when registering your application
::
  url, state = mhOauthObject.authorize_token_url(mh_callback_url)
Let the user open the *url*. Save the *state* to the database.
call_back_url is the url that you set when registering your app.
The user will be redirected to it after giving the app access to
their account. Under Armour will do a get request to that url
with a code. The code is used to get the token.
::
  tokenInfo = mhOauthObject.fetch_access_token(code)

tokenInfo contains all the info needed (access token, refresh token, etc.)
When getting the token info from Under Armour, save it to the database for later use.
::
  mhObject = MH(client_id = mh_key, client_secret = mh_secret, access_token=access_token)
Call the *mhObject* methods to interact with Under Armour API.
Example:
::
  profile = mhObject.user_profile_get(user_id=mh_user_id)

For any methods that are not included in the library:
::
  result = mhObject.make_request(url, method, data)

The methods and *data* format could be found at:
`https://developer.underarmour.com/docs/`

----

**License**

MIT License

see: 'https://github.com/igorfala/python-under-armour/blob/master/LICENSE'