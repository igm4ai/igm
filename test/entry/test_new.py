import os.path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from igm.entry.cli import get_cli_entry
from ..testings import TEMPLATE_SIMPLE, TEMPLATE_TEST


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

                    '```shell',
                    'igm run',
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

    def test_new_cancelled(self, sys_config_1, hansbug_env):
        runner = CliRunner(mix_stderr=False)
        template_test = os.path.abspath(TEMPLATE_TEST)

        with runner.isolated_filesystem(), patch.dict('os.environ', {'CANCEL': '1'}, clear=False):
            result = runner.invoke(get_cli_entry(), args=[
                'new', template_test, 'test_project'])

            assert result.exit_code == 0x11
            assert result.stdout.strip() == 'Cancelled.'
            assert result.stderr.strip() == 'Project creation cancelled.'
