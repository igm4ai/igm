import os.path
from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from igm.entry.cli import get_cli_entry
from ..testings import TEMPLATE_SIMPLE, CPU_INFO_1, MEMORY_INFO_2, CPU_INFO_100, MEMORY_INFO_100, TWO_GPU_DATA


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


@pytest.mark.unittest
class TestEntryNew:
    def test_new(self, sys_config_1, hansbug_env):
        runner = CliRunner(mix_stderr=False)
        template_simple = os.path.abspath(TEMPLATE_SIMPLE)

        with runner.isolated_filesystem():
            result = runner.invoke(get_cli_entry(), args=[
                'new', template_simple, 'test_project'])

            assert result.exit_code == 0
            assert os.path.exists('test_project')
            assert os.path.isdir('test_project')

            assert os.path.exists('test_project/main.py')
            with open('test_project/main.py', 'r') as rf:
                lines = list(filter(bool, map(str.strip, rf.readlines())))
                assert lines == [
                    'cpus = 6',
                    "mem_size = '63.76 GiB'",
                    "os = 'Windows'",
                    "python = 'PyPy 3.7.12'",

                    "print('This is your first try!')",
                    "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')"
                ]

            with open('test_project/README.md', 'r') as rf:
                lines = list(filter(bool, map(str.strip, rf.readlines())))
                assert lines == [
                    '# hello world for hansbug',
                    "This is a hello world project of igm created by 'hansbug' (age: `18`).",
                    'You can start this project by the following command:',

                    '```python',
                    'python main.py',
                    '```'
                ]

    def test_new_dir_exist(self, sys_config_1, hansbug_env):
        runner = CliRunner(mix_stderr=False)
        template_simple = os.path.abspath(TEMPLATE_SIMPLE)

        with runner.isolated_filesystem():
            os.makedirs('test_project')
            result = runner.invoke(get_cli_entry(), args=[
                'new', template_simple, 'test_project'])

            assert result.exit_code == 0x10
            assert 'Path \'test_project\' already exist, unable to create project.' in result.stderr
