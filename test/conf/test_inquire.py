import pytest

from igm.conf import with_user_inquire
from igm.env import user


@pytest.mark.unittest
class TestConfInquire:
    def test_with_user_inquire(self):
        assert not user
        assert len(user) == 0
        with pytest.raises(KeyError):
            _ = user['a']
        with pytest.raises(AttributeError):
            _ = user.a

        with with_user_inquire({'a': 1, 'b': 'hansbug'}):
            assert user
            assert len(user) == 2
            assert user.a == 1
            assert user['a'] == 1
            assert user.b == 'hansbug'
            assert user['b'] == 'hansbug'
