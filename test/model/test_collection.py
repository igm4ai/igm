import pytest

from igm.model import GenericCollection


@pytest.fixture()
def demo_collection():
    return GenericCollection([2, 3, 5, 7])


@pytest.fixture()
def demo_empty_collection():
    return GenericCollection([])


@pytest.mark.unittest
class TestModelCollection:
    def test_len(self, demo_collection):
        assert len(demo_collection) == 4

    def test_getitem(self, demo_collection):
        assert demo_collection[0] == 2
        assert demo_collection[1] == 3
        assert demo_collection[-1] == 7
        assert demo_collection[::2] == [2, 5]

    def test_num(self, demo_collection):
        return demo_collection.num == 4

    def test_str(self, demo_collection):
        assert str(demo_collection) == 'GenericCollection([2, 3, 5, 7])'

    def test_repr(self, demo_collection):
        assert repr(demo_collection) == 'GenericCollection([2, 3, 5, 7])'

    def test_bool(self, demo_collection, demo_empty_collection):
        assert demo_collection
        assert not demo_empty_collection
