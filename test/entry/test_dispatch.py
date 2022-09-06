import pytest
from click.testing import CliRunner

from igm.config.meta import __TITLE__, __VERSION__
from igm.entry import cli_entry


@pytest.mark.unittest
class TestEntryDispatch:
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli_entry, args=['-v'])

        assert result.exit_code == 0
        assert __TITLE__.lower() in result.stdout.lower()
        assert __VERSION__.lower() in result.stdout.lower()

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli_entry, args=['-h'])

        assert result.exit_code == 0
        assert 'show igm\'s version information' in result.stdout.lower()
        assert '-h, --help' in result.stdout.lower()
