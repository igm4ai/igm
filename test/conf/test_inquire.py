import pytest
from hbutils.testing import capture_output

from igm.conf.inquire import with_user_inquire, inquire_call, InquireCancel, InquireRestart
from igm.env import user


@pytest.fixture()
def normal():
    def _func():
        return {'a': 1, 'b': 2}

    return _func


@pytest.fixture()
def cancel():
    def _func():
        raise InquireCancel('cancel reason')

    return _func


@pytest.fixture()
def key_interrupt():
    def _func():
        raise KeyboardInterrupt

    return _func


@pytest.fixture()
def restart():
    cnt = -1

    def _func():
        nonlocal cnt
        cnt += 1
        if cnt < 2:
            raise InquireRestart
        elif cnt < 5:
            raise InquireRestart(f'reason for #{cnt}')

        return {'cnt': cnt ** 2}

    return _func


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

    def test_inquire_call(self, normal, cancel, key_interrupt, restart):
        ok, retval = inquire_call(normal)
        assert ok
        assert retval == {'a': 1, 'b': 2}

        with capture_output() as co:
            ok, retval = inquire_call(cancel)
        assert not ok
        assert retval is None
        assert co.stdout.strip() == 'Cancelled: cancel reason.'

        with capture_output() as co:
            ok, retval = inquire_call(key_interrupt)
        assert not ok
        assert retval is None
        assert co.stdout.strip() == 'Cancelled.'

        with capture_output() as co:
            ok, retval = inquire_call(restart)
        assert ok
        assert retval == {'cnt': 25}
        assert list(map(str.strip, co.stdout.splitlines())) == [
            'Restarting...',
            'Restarting...',
            'Restarting... reason for #2',
            'Restarting... reason for #3',
            'Restarting... reason for #4',
        ]
