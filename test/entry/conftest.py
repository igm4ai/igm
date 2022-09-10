import os
import shlex
from contextlib import contextmanager
from unittest.mock import patch, MagicMock

import pytest

from igm.conf import load_igm_setup
from igm.utils.retrieve import LocalTemporaryDirectory
from ..testings import CPU_INFO_1, MEMORY_INFO_2, CPU_INFO_100, MEMORY_INFO_100, TWO_GPU_DATA, TEMPLATE_SIMPLE, \
    TEMPLATE_TEST


@pytest.fixture()
def sys_config_1():
    with patch('igm.env.system.get_cpu_info', MagicMock(return_value=CPU_INFO_1)), \
            patch('igm.env.system.get_memory_info', MagicMock(return_value=MEMORY_INFO_2)), \
            patch('platform.python_version', MagicMock(return_value='3.7.12')), \
            patch('platform.python_implementation', MagicMock(return_value='Pypy')), \
            patch('platform.system', MagicMock(return_value='Windows')), \
            patch('igm.env.hardware.nvidia.which', MagicMock(return_value=None)):
        yield


@pytest.fixture()
def sys_config_2():
    with patch('igm.env.system.get_cpu_info', MagicMock(return_value=CPU_INFO_100)), \
            patch('igm.env.system.get_memory_info', MagicMock(return_value=MEMORY_INFO_100)), \
            patch('platform.python_version', MagicMock(return_value='3.9.4')), \
            patch('platform.python_implementation', MagicMock(return_value='CPython')), \
            patch('platform.system', MagicMock(return_value='macos')), \
            patch('igm.env.system.get_nvidia_info', MagicMock(return_value=TWO_GPU_DATA)):
        yield


@pytest.fixture()
def hansbug_env():
    with patch.dict(os.environ, {'NAME': 'hansbug', 'AGE': '18', 'GENDER': 'Male', 'NON_CONFIRM': '1'}, clear=False):
        yield


@pytest.fixture()
def time_2022_9_9():
    with patch('time.time', MagicMock(return_value=1662714925.0)):
        yield


@pytest.fixture()
def simple_project(hansbug_env, sys_config_1, time_2022_9_9):
    with LocalTemporaryDirectory() as tdir:
        with load_igm_setup(TEMPLATE_SIMPLE, silent=True) as t:
            proj_dir = os.path.join(tdir, 'simple')
            assert t.run(proj_dir, silent=True)

            yield proj_dir


@pytest.fixture()
def test_project(hansbug_env, sys_config_1, time_2022_9_9):
    with LocalTemporaryDirectory() as tdir:
        with load_igm_setup(TEMPLATE_TEST, silent=True) as t:
            proj_dir = os.path.join(tdir, 'test')
            assert t.run(proj_dir, silent=True)

            yield proj_dir


@pytest.fixture()
def mock_argv(args):
    if isinstance(args, str):
        args = shlex.split(args)

    with patch('sys.argv', args):
        yield


@pytest.fixture()
def mock_exitcode():
    def _fake_func(x=None):
        raise SystemExit(x or 0)

    _exitcode = None

    def _get_exitcode():
        return _exitcode

    @contextmanager
    def _mocker():
        try:
            with patch('sys.exit', _fake_func):
                yield _get_exitcode
        except SystemExit as err:
            nonlocal _exitcode
            _exitcode = err.code

    return _mocker
