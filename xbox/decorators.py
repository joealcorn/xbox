from xbox import client


def authenticates(func):
    def inner(*a, **kw):
        if not client.authenticated:
            client.authenticate()
        return func(*a, **kw)

    return inner
