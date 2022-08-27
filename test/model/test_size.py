import pytest

from igm.model import SizeScale


@pytest.fixture()
def size_172mb():
    return SizeScale('17.2MiB')


class _SizePlus(SizeScale):
    pass


@pytest.fixture()
def size_plus_172mb():
    return _SizePlus('17.2MiB')


@pytest.fixture()
def size_0():
    return SizeScale(0)


@pytest.mark.unittest
class TestModelSize:
    def test_init(self):
        assert SizeScale(23890749823).bytes == 23890749823
        assert SizeScale('932.23 MiB').bytes == 977514004
        assert SizeScale(SizeScale('932.23 MiB')).bytes == 977514004

    def test_bytes(self, size_172mb):
        assert size_172mb.bytes == 18035507

    def test_int(self, size_172mb):
        assert int(size_172mb) == 18035507

    def test_index(self, size_172mb):
        assert size_172mb.__index__() == 18035507

    def test_str(self, size_172mb, size_plus_172mb):
        assert str(size_172mb) == '17.20 MiB'
        assert str(size_plus_172mb) == '17.20 MiB'

    def test_repr(self, size_172mb, size_plus_172mb):
        assert repr(size_172mb) == '<SizeScale 17.20 MiB>'
        assert repr(size_plus_172mb) == '<_SizePlus 17.20 MiB>'

    def test_cmp(self, size_172mb, size_plus_172mb):
        assert size_172mb == size_plus_172mb
        assert size_172mb == 18035507
        assert size_172mb > '17.1 MB'
        assert size_172mb >= '17.1 MB'
        assert size_172mb < '17.3 MiB'
        assert size_172mb <= '17.3 MiB'
        assert size_172mb != 18035505
        assert size_172mb != None

    def test_bool(self, size_172mb, size_plus_172mb, size_0):
        assert size_172mb
        assert size_plus_172mb
        assert not size_0
