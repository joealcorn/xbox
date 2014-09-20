import os

from betamax import Betamax
import pytest

import xbox
from xbox.tests import TestBase


def track_calls(func):
    def inner(*a, **kw):
        inner.called = True
        inner.calls.append((a, kw))
        return func(*a, **kw)

    if not hasattr(inner, 'called'):
        inner.called = False

    if not hasattr(inner, 'calls'):
        inner.calls = []

    return inner


class TestDecorators(TestBase):

    def test_authenticated_decorator_success(self):
        xbox.client.authenticate = track_calls(xbox.client.authenticate)

        assert not xbox.client.authenticate.called
        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']
            os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'
            os.environ['MS_PASSWD'] = 'password'
            vcr.use_cassette(
                'authenticate_decorator_success',
                match_on=match_on,
                record_mode='never',
            )

            xbox.GamerProfile.from_gamertag('JoeAlcorn')

            assert xbox.client.authenticated
            assert xbox.client.login == 'pyxb-testing@outlook.com'
            assert xbox.client.authenticate.called

            xbox.GamerProfile.from_gamertag('JoeAlcorn')
            assert len(xbox.client.authenticate.calls) == 1

    def test_authenticated_decorator_failure(self):
        xbox.client.authenticate = track_calls(xbox.client.authenticate)
        assert not xbox.client.authenticate.called

        os.environ['MS_LOGIN'] = 'pyxb-testing@outlook.com'

        with pytest.raises(xbox.exceptions.AuthenticationException):
            xbox.GamerProfile.from_gamertag('JoeAlcorn')

        with Betamax(xbox.client.session) as vcr:
            match_on = ['uri', 'method', 'headers', 'body']
            vcr.use_cassette(
                'authenticate_decorator_failure',
                match_on=match_on,
                record_mode='never',
            )

            os.environ['MS_PASSWD'] = 'password'

            with pytest.raises(xbox.exceptions.AuthenticationException):
                xbox.GamerProfile.from_gamertag('JoeAlcorn')

        assert len(xbox.client.authenticate.calls) == 2
