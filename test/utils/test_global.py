import os

import pytest


def relpath(*path):
    return os.path.normpath(os.path.join(__file__, '..', *path))


@pytest.mark.unittest
class TestUtilsGlobal:
    def test_get_global_env_simple(self):
        d1 = {}
        with open(relpath('gf1.py'), 'r') as sf:
            exec(sf.read(), d1)

        assert d1['TT'] == 233
        assert d1['TTX'] == 233
        assert d1['TF'] == 8
        assert d1['TF1'] == 8
        assert d1['TF2'] == 8

        d2 = {'value': 142857}
        with open(relpath('gf1.py'), 'r') as sf:
            exec(sf.read(), d2)

        assert d2['TT'] == 142857
        assert d2['TTX'] == 233
        assert d2['TF'] == 2915443148696793
        assert d2['TF1'] == 2915443148696793
        assert d2['TF2'] == 2915443148696793

    def test_globals(self):
        d1 = {}
        with open(relpath('gf2.py'), 'r') as sf:
            exec(sf.read(), d1)

        assert d1['v'] == 233
