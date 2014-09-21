
class XboxException(Exception):
    '''
    Base exception for all Xbox exceptions
    to subclass
    '''


class AuthenticationException(XboxException):
    '''
    Raised when logging in fails, likely due to
    incorrect auth credentials
    '''


class InvalidRequest(XboxException):
    '''
    Something is wrong with the request

    :var message: Error message returned by server is possible
    :var response: requests response object

    '''
    def __init__(self, message, response):
        self.message = message
        self.response = response


class NotFoundException(XboxException):
    '''
    Any exception raised due to a resource
    being missing will subclass this
    '''


class GamertagNotFound(NotFoundException):
    pass


class ClipNotFound(NotFoundException):
    pass
