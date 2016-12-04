class HTTPBadRequest(Exception):
    """400 - Bad Request:
    The request was invalid. This response code is common when required
    fields are unspecified, formatted incorrectly,
    or invalid filters are requested.
    """
    pass


class HTTPUnauthorized(Exception):
    """401 - Unauthorized:
    The request authentication failed. The OAuth credentials that
    the client supplied were missing or invalid.
    """
    pass


class HTTPForbidden(Exception):
    """403 - Forbidden:
    The request credentials authenticated, but the requesting
    user or client app is not authorized to access the given resource.
    """
    pass


class HTTPNotFound(Exception):
    """404 - Not Found:
    The requested resource does not exist.
    """
    pass


class HTTPMethodNotAllowed(Exception):
    """405 - Method Not Allowed:
    The requested HTTP method is invalid for the given resource.
    Review the resource documentation for supported methods.
    """
    pass


class HTTPServerError(Exception):
    """500 - Server Error:
    The server failed to fulfill the request.
    Please notify support with details of the request
    and response so that we can fix the problem.
    """
    pass
