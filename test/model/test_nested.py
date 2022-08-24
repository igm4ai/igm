from collections import namedtuple

import pytest

from igm.model import MappingBasedModel, SequenceBasedModel

ntp = namedtuple('ntp', ['name', 'gender', 'age'])


@pytest.fixture()
def demo_nested_dict():
    return MappingBasedModel({
        'a': 233,
        'b': [3, 4, 5, {'t': 5, 'y': {'z': 2}, 'f': (3, 4)}],
        'c': {'x': 3490, 'y': (5, 6, 7)},
        'z': ntp('hansbug', 'male', 20000),
    })


@pytest.fixture()
def demo_nested_list(demo_nested_dict):
    return demo_nested_dict['b']


@pytest.fixture()
def demo_namedtuple(demo_nested_dict):
    return demo_nested_dict['z']


@pytest.mark.unittest
class TestModelNested:
    def test_dict(self, demo_nested_dict):
        assert demo_nested_dict['a'] == 233
        assert demo_nested_dict.a == 233
        assert demo_nested_dict.b[0] == 3
        assert len(demo_nested_dict) == 4
        assert set(demo_nested_dict.keys()) == {'a', 'b', 'c', 'z'}
        assert str(demo_nested_dict).startswith('{') and str(demo_nested_dict).endswith('}')
        assert repr(demo_nested_dict).startswith('MappingBasedModel({') and repr(demo_nested_dict).endswith('})')
        assert demo_nested_dict == {
            'a': 233,
            'b': [3, 4, 5, {'t': 5, 'y': {'z': 2}, 'f': (3, 4)}],
            'c': {'x': 3490, 'y': (5, 6, 7)},
            'z': ntp('hansbug', 'male', 20000),
        }
        assert demo_nested_dict == MappingBasedModel({
            'a': 233,
            'b': [3, 4, 5, {'t': 5, 'y': {'z': 2}, 'f': (3, 4)}],
            'c': {'x': 3490, 'y': (5, 6, 7)},
            'z': ntp('hansbug', 'male', 20000),
        })
        assert demo_nested_dict != {
            'a': 233,
            'b': [3, 4, 5, {'t': 5, 'y': {'z': 2}, 'f': (3, 4)}],
            'c': {'x': 3490, 'y': (5, 6, 7)},
            'z': ntp('hansbug', 'male', 20001),
        }
        assert demo_nested_dict != None

    def test_seq(self, demo_nested_list):
        assert demo_nested_list[0] == 3
        assert isinstance(demo_nested_list[-1], MappingBasedModel)
        assert demo_nested_list[-1] == {'t': 5, 'y': {'z': 2}, 'f': (3, 4)}
        assert len(demo_nested_list) == 4
        assert demo_nested_list == [3, 4, 5, {'t': 5, 'y': {'z': 2}, 'f': (3, 4)}]
        assert demo_nested_list == SequenceBasedModel([3, 4, 5, {'t': 5, 'y': {'z': 2}, 'f': (3, 4)}])
        assert demo_nested_list != [3, 4, 5, {'t': 5, 'y': {'z': 2}, 'f': (3, 5)}]
        assert demo_nested_list != None
        assert demo_nested_list != 'sdkfjklsd'
        assert str(demo_nested_list) == '[3, 4, 5, {\'t\': 5, \'y\': {\'z\': 2}, \'f\': (3, 4)}]'
        assert repr(demo_nested_list) == 'SequenceBasedModel([3, 4, 5, {\'t\': 5, \'y\': {\'z\': 2}, \'f\': (3, 4)}])'

    def test_named_tuple(self, demo_namedtuple):
        assert demo_namedtuple[0] == 'hansbug'
        assert demo_namedtuple.name == 'hansbug'
        assert demo_namedtuple[1] == 'male'
        assert demo_namedtuple.gender == 'male'
        assert demo_namedtuple[2] == 20000
        assert demo_namedtuple.age == 20000
        assert len(demo_namedtuple) == 3
        assert str(demo_namedtuple) == 'ntp(name=\'hansbug\', gender=\'male\', age=20000)'
        assert repr(demo_namedtuple) == 'SequenceBasedModel(ntp(name=\'hansbug\', gender=\'male\', age=20000))'
