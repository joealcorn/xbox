
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


class NotFoundException(XboxException):
    '''
    Any exception raised due to a resource
    being missing will subclass this
    '''


class GamertagNotFound(NotFoundException):
    pass


class ClipNotFound(NotFoundException):
    pass
