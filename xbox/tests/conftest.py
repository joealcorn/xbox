import os
import json

from betamax import Betamax
import pytest

from xbox.resource import Clip, GamerProfile

here = lambda path: '%s/%s' % (os.path.dirname(__file__), path)


with Betamax.configure() as config:
    config.cassette_library_dir = here('files/cassettes')


@pytest.fixture
def clip():
    with open(here('files/clip.json')) as f:
        data = json.loads(f.read())

    return Clip(user=None, clip_data=data)


@pytest.fixture
def gamerprofile():
    with open(here('files/user.json')) as f:
        data = json.loads(f.read())

    _user = data['profileUsers'][0]
    xuid = _user['id']
    settings = _user['settings']

    return GamerProfile(xuid, settings, data)
