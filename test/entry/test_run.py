import os.path

import pytest
from hbutils.testing import simulate_entry, isolated_directory

from igm.entry.cli import get_cli_entry


@pytest.fixture()
def simple_project_dir(simple_project):
    orddir = os.path.abspath(os.curdir)
    try:
        os.chdir(simple_project)
        yield simple_project
    finally:
        os.chdir(orddir)


@pytest.fixture()
def test_project_dir(test_project):
    orddir = os.path.abspath(os.curdir)
    try:
        os.chdir(test_project)
        yield test_project
    finally:
        os.chdir(orddir)


@pytest.fixture()
def project_without_default_dir():
    with isolated_directory():
        with open('igmeta.py', 'w+') as f:
            print("""
import sys
from igm.conf import igm_project, cpy, cpip

def f():
    raise ValueError(233)

igm_project(
    name='hansbug-demo',
    version='0.3.2',
    template_name='test',
    template_version='0.0.1',
    created_at=1662902108.913866,
    scripts={
        'version': cpip('-V'),
        'echo': 'echo 6 cpus',
        'echox': ['echo', '1', '2', '3', '4'],
        'f': f,
    }
)
            """, file=f)

        yield os.path.abspath(os.curdir)


@pytest.fixture()
def empty_dir():
    with isolated_directory():
        yield os.path.abspath(os.curdir)


@pytest.fixture()
def invalid_dir():
    with isolated_directory():
        with open('igmeta.py', 'w+') as f:
            print('VALUE = 1', file=f)

        yield os.path.abspath(os.curdir)


@pytest.mark.unittest
class TestEntryRun:
    def test_simple_default(self, simple_project_dir):
        result = simulate_entry(get_cli_entry(), ['igm', 'run'])
        result.assert_okay()
        stdout_lines = list(filter(bool, map(str.strip, result.stdout.splitlines())))
        assert stdout_lines[1:] == [
            'This is your first try!',
            'UR running PyPy 3.7.12 on Windows, with a 6 core 63.76 GiB device.',
        ]
        assert result.stderr.strip() == ''

        result = simulate_entry(get_cli_entry(), ['igm', 'run', '-L'])
        result.assert_okay()
        stdout_lines = list(filter(bool, map(str.strip, result.stdout.splitlines())))
        assert stdout_lines == [
            'This is your first try!',
            'UR running PyPy 3.7.12 on Windows, with a 6 core 63.76 GiB device.',
        ]
        assert result.stderr.strip() == ''

    def test_test_default(self, test_project_dir):
        result = simulate_entry(get_cli_entry(), ['igm', 'run'])
        result.assert_okay()
        stdout_lines = list(filter(bool, map(str.strip, result.stdout.splitlines())))
        assert stdout_lines[1:] == [
            'This is your first try!',
            'UR running PyPy 3.7.12 on Windows, with a 6 core 63.76 GiB device.',
        ]
        assert result.stderr.strip() == ''

        result = simulate_entry(get_cli_entry(), ['igm', 'run', '-L'])
        result.assert_okay()
        stdout_lines = list(filter(bool, map(str.strip, result.stdout.splitlines())))
        assert stdout_lines == [
            'This is your first try!',
            'UR running PyPy 3.7.12 on Windows, with a 6 core 63.76 GiB device.',
        ]
        assert result.stderr.strip() == ''

    def test_test_subcommands(self, test_project_dir):
        result = simulate_entry(get_cli_entry(), ['igm', 'run', 'func'])
        result.assert_okay()
        stdout_lines = list(filter(bool, map(str.strip, result.stdout.splitlines())))
        assert stdout_lines == ['Call function \'_my_func\'.', 'This is my func']

        result = simulate_entry(get_cli_entry(), ['igm', 'run', 'func', '-L'])
        result.assert_okay()
        stdout_lines = list(filter(bool, map(str.strip, result.stdout.splitlines())))
        assert stdout_lines == ['This is my func']

    def test_test_print_error(self, test_project_dir):
        result = simulate_entry(get_cli_entry(), ['igm', 'run', 'e1'])
        assert result.exitcode == 0x1
        assert result.error is None
        assert result.stdout.strip() == 'Call function \'e1\'.'
        assert result.stderr.strip().splitlines(keepends=False)[-1] == 'ValueError'

        result = simulate_entry(get_cli_entry(), ['igm', 'run', 'e2'])
        assert result.exitcode == 0x1
        assert result.error is None
        assert result.stdout.strip() == 'Call function \'e2\'.'
        assert result.stderr.strip().splitlines(keepends=False)[-1] == 'KeyError: key error'

        result = simulate_entry(get_cli_entry(), ['igm', 'run', 'e3'])
        assert result.exitcode == 0x1
        assert result.error is None
        assert result.stdout.strip() == 'Call function \'e3\'.'
        assert result.stderr.strip().splitlines(keepends=False)[-1] == 'TypeError: (\'type\', \'error\', 233)'

    def test_fake_without_default(self, project_without_default_dir):
        result = simulate_entry(get_cli_entry(), ['igm', 'run'])
        assert result.exitcode == 0x31
        assert result.error is None
        assert result.stdout.strip() == ''

        stderr_lines = list(filter(bool, map(str.strip, result.stderr.splitlines())))
        assert stderr_lines == [
            'No default script in this project.',
            "If you need to assign one, just set its name to 'None'."
        ]

    def test_fake_raise_error(self, project_without_default_dir):
        result = simulate_entry(get_cli_entry(), ['igm', 'run', 'f'])
        assert result.exitcode == 0x1
        assert result.error is None
        assert result.stdout.strip() == 'Call function \'f\'.'
        assert 'Unexpected error found when running IGM CLI!' in result.stderr
        assert 'ValueError: 233' in result.stderr

    def test_not_project_dir(self, empty_dir):
        result = simulate_entry(get_cli_entry(), ['igm', 'run'])
        assert result.exitcode == 0x30
        assert result.error is None
        assert result.stdout.strip() == ''
        assert result.stderr.strip() == 'Not an IGM project here.'

    def test_invalid_project_dir(self, invalid_dir):
        result = simulate_entry(get_cli_entry(), ['igm', 'run'])
        assert result.exitcode == 0x30
        assert result.error is None
        assert result.stdout.strip() == ''
        assert result.stderr.strip() == 'Not an IGM project here.'
