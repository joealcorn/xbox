import xbox


def authenticates(func):
    def inner(*a, **kw):
        if not xbox.client.authenticated:
            xbox.client.authenticate()
        return func(*a, **kw)

    return inner
