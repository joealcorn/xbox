import pickle

from xbox.vendor import six
from xbox.tests import TestBase


class TestPickle(TestBase):

    def test_pickle_clip(self, clip):
        pickled = pickle.dumps(clip)
        restored = pickle.loads(pickled)
        assert id(clip) != id(restored)
        for key, value in six.iteritems(clip.__dict__):
            assert restored.__dict__[key] == value

    def test_pickle_gamer_profile(self, gamerprofile):
        pickled = pickle.dumps(gamerprofile)
        restored = pickle.loads(pickled)
        assert id(gamerprofile) != id(restored)
        for key, value in six.iteritems(gamerprofile.__dict__):
            assert restored.__dict__[key] == value
