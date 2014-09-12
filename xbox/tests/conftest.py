import os
import json

import pytest

from xbox.resource import Clip

here = lambda path: '%s/%s' % (os.path.dirname(__file__), path)


@pytest.fixture
def clip():
    with open(here('files/clip.json')) as f:
        data = json.loads(f.read())

    return Clip(user=None, clip_data=data)
