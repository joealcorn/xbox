import os

import xbox


class TestBase(object):

    def setup_method(self, method):
        # reset the client instance
        xbox.client = xbox.Client()

        # reset auth creds
        os.environ.pop('MS_LOGIN', None)
        os.environ.pop('MS_PASSWD', None)
