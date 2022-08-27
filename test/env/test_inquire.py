from collections import namedtuple

import pytest

from igm.env import user
from igm.env.inquire import user_inq_with

_MyTuple = namedtuple('_MyTuple', ['a', 'b'])


@pytest.fixture()
def inquire_set_1():
    with user_inq_with({'a': 1, 'b': 'dslkfdjs', 'c': {'f': 2}, 'd': [1, 4, 'sdfjk'], 'e': _MyTuple(3, 12)}):
        yield


@pytest.fixture()
def inquire_set_empty():
    with user_inq_with({}):
        yield


@pytest.mark.unittest
class TestEnvInquire:
    def test_inquire_set_1(self, inquire_set_1):
        assert user
        assert len(user) == 5
        assert list(iter(user)) == ['a', 'b', 'c', 'd', 'e']
        assert user.a == 1
        assert user['a'] == 1
        assert user.b == 'dslkfdjs'
        assert user['b'] == 'dslkfdjs'
        assert user.c == {'f': 2}
        assert user['c'] == {'f': 2}
        assert user.d == [1, 4, 'sdfjk']
        assert user['d'] == [1, 4, 'sdfjk']
        assert user.e == _MyTuple(3, 12)
        assert user['e'] == _MyTuple(3, 12)
        assert str(user) == 'UserInquire({\'a\': 1, \'b\': \'dslkfdjs\', \'c\': {\'f\': 2}, ' \
                            '\'d\': [1, 4, \'sdfjk\'], \'e\': _MyTuple(a=3, b=12)})'
        assert repr(user) == 'UserInquire({\'a\': 1, \'b\': \'dslkfdjs\', \'c\': {\'f\': 2}, ' \
                             '\'d\': [1, 4, \'sdfjk\'], \'e\': _MyTuple(a=3, b=12)})'

    def test_inquire_set_empty(self, inquire_set_empty):
        assert not user
        assert len(user) == 0
        assert list(iter(user)) == []

        with pytest.raises(AttributeError):
            _ = user.a
        with pytest.raises(KeyError):
            _ = user['a']

        assert str(user) == 'UserInquire({})'
        assert repr(user) == 'UserInquire({})'
