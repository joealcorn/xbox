
class DotNotationDict(dict):
    '''
    Dictionary subclass that allows attribute
    access using dot notation, eg:

    >>> dnd = DotNotationDict({'test': True})
    >>> dnd.test
    True
    '''

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("DotNotationDict has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value
