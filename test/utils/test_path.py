import pytest

from igm.utils import normpath


@pytest.mark.unittest
class TestUtilsPath:
    def test_normpath(self):
        assert normpath('1/2') == normpath('1', '2')
        assert normpath('1/../3') == normpath('3')
        assert normpath('1/../3') != normpath('1/3')
