import pytest

from xbox.utils import DotNotationDict


def test_dot_notation_dict_raises_attribute_error():
    d = DotNotationDict()
    with pytest.raises(AttributeError):
        d.error
