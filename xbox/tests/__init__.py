import xbox


class TestBase(object):

    def setup_method(self, method):
        # reset the client instance
        xbox.client = xbox.Client()
