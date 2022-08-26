from unittest.mock import patch, MagicMock

import pytest


@pytest.fixture()
def cpython_3_7_12():
    with patch('platform.python_version', MagicMock(return_value='3.7.12')), \
            patch('platform.python_implementation', MagicMock(return_value='CPython')):
        yield


@pytest.fixture()
def pypy_3_9_2():
    with patch('platform.python_version', MagicMock(return_value='3.9.2')), \
            patch('platform.python_implementation', MagicMock(return_value='PyPy')):
        yield


@pytest.fixture()
def pip_19_2_3():
    with patch.dict('hbutils.system.python.package.PIP_PACKAGES', {'pip': '19.2.3'}, clear=False):
        yield


@pytest.fixture()
def hbutils_7_9_10():
    with patch.dict('hbutils.system.python.package.PIP_PACKAGES', {'hbutils': '7.9.10'}, clear=False):
        yield
