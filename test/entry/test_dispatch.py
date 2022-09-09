import pytest
from click.testing import CliRunner
from hbutils.testing import capture_output

from igm.config.meta import __TITLE__, __VERSION__
from igm.entry import cli_entry
from igm.entry.cli import get_cli_entry


@pytest.mark.unittest
class TestEntryDispatch:
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(get_cli_entry(), args=['-v'])

        assert result.exit_code == 0
        assert __TITLE__.lower() in result.stdout.lower()
        assert __VERSION__.lower() in result.stdout.lower()

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(get_cli_entry(), args=['-h'])

        assert result.exit_code == 0
        assert 'show igm\'s version information' in result.stdout.lower()
        assert '-h, --help' in result.stdout.lower()

    @pytest.mark.parametrize(['args', ], [(['igm', '-v'],)])
    def test_actual_version(self, mock_argv, mock_exitcode):
        with capture_output() as co:
            with mock_exitcode() as _get_exitcode:
                cli_entry()

        assert _get_exitcode() == 0
        assert __TITLE__.lower() in co.stdout.lower()
        assert __VERSION__.lower() in co.stdout.lower()

    @pytest.mark.parametrize(['args', ], [(['igm', '-h'],)])
    def test_actual_version(self, mock_argv, mock_exitcode):
        with capture_output() as co:
            with mock_exitcode() as _get_exitcode:
                cli_entry()

        assert _get_exitcode() == 0
        assert 'show igm\'s version information' in co.stdout.lower()
        assert '-h, --help' in co.stdout.lower()
