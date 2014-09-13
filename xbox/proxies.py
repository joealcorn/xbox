import operator

from xbox.vendor import six


def object_proxy(func):
    def inner(self, *a, **kw):
        if not self._resolved:
            self.resolved_object = self.resolve()
        return func(self.resolved_object, *a, **kw)
    return inner


class LazyProxy(object):
    '''
    Base class for creating lazily evaluated objects.
    Subclass must override resolve method and return
    the resolved object.
    '''
    _resolved = False

    def __init__(self, **kw):
        for key, val in six.iteritems(kw):
            setattr(self, key, val)

    def resolve(self):
        raise NotImplementedError

    __getattr__ = object_proxy(getattr)
    __delattr__ = object_proxy(delattr)
    __dir__ = object_proxy(dir)

    if six.PY3:
        __bytes__ = object_proxy(bytes)
        __str__ = object_proxy(str)
        __bool__ = object_proxy(bool)
    else:
        __str__ = object_proxy(str)
        __unicode__ = object_proxy(unicode)
        __nonzero__ = object_proxy(bool)

    # pretend to be the proxied class in case anything cares about this
    __class__ = property(object_proxy(operator.attrgetter("__class__")))
    __eq__ = object_proxy(operator.eq)
    __ne__ = object_proxy(operator.ne)
    __hash__ = object_proxy(hash)

    # Dictionary methods support
    __getitem__ = object_proxy(operator.getitem)
    __setitem__ = object_proxy(operator.setitem)
    __delitem__ = object_proxy(operator.delitem)

    __len__ = object_proxy(len)
    __contains__ = object_proxy(operator.contains)

    def __setattr__(self, key, value):
        if key == 'resolved_object':
            # prevent infinite recursion
            self.__dict__[key] = value
            return

        if not self._resolved:
            self.resolved_object = self.resolve()
        setattr(self.resolved_object, key, value)

    def __str__(self):
        # return proxied __str__ if it's resolved,
        # but don't resolve it just for this
        if getattr(self, '_resolved', False):
            return self.resolved_object.__str__()
        else:
            return super(LazyProxy, self).__str__()


class UserProxy(LazyProxy):
    def __init__(self, xuid):
        self.__dict__['xuid'] = xuid

    def resolve(self):
        from xbox.resource import GamerProfile
        xuid = self.__dict__['xuid']

        gt = GamerProfile.from_xuid(xuid)
        self.__dict__['_resolved'] = True
        return gt
