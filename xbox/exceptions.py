
class XboxException(Exception):
    '''
    Base exception for all Xbox exceptions
    to subclass
    '''


class AuthenticationException(XboxException):
    pass


class NotFoundException(XboxException):
    '''
    Any exception raised due to a resource
    being missing will subclass this
    '''


class GamertagNotFound(NotFoundException):
    pass
