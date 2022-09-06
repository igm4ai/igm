import os
from unittest import skipUnless

import pytest
from click.testing import CliRunner

from igm.entry import cli_entry
from ..testings import TEMPLATE_SIMPLE, TEMPLATE_SIMPLE_REPO_GIT, get_testfile_url


@pytest.mark.unittest
class TestEntryShow:
    def test_show_local(self):
        runner = CliRunner()
        result = runner.invoke(cli_entry, args=['show', TEMPLATE_SIMPLE])

        assert result.exit_code == 0
        assert 'Template: simple' in result.stdout
        assert 'Version: 0.0.1' in result.stdout
        assert 'Description: ' in result.stdout

    @pytest.mark.parametrize(['silent'], [(True,), (False,)])
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    def test_show_git_silent(self, silent):
        runner = CliRunner()
        result = runner.invoke(cli_entry, args=[
            'show', TEMPLATE_SIMPLE_REPO_GIT,
            *(('--silent',) if silent else ())
        ])

        assert result.exit_code == 0
        if silent:
            assert 'Cloning' not in result.stdout
            assert 'Downloading' not in result.stdout
            assert 'Unpacking' not in result.stdout
        else:
            assert 'Cloning' in result.stdout
            assert 'Downloading' not in result.stdout
            assert 'Unpacking' not in result.stdout

        assert 'Template: simple' in result.stdout
        assert 'Version: 0.0.1' in result.stdout
        assert 'Description: ' in result.stdout

    @pytest.mark.parametrize(
        ['fmt', 'ext', 'silent'],
        [
            ('7z', '.7z', True),
            ('rar', '.rar', False),
            ('bztar', '.tar.bz2', True),
            ('gztar', '.tar.gz', False),
            ('tar', '.tar', True),
            ('xztar', '.tar.xz', False),
            ('zip', '.zip', True),
        ]
    )
    def test_show_local_archive(self, fmt, ext, silent):
        runner = CliRunner()
        result = runner.invoke(cli_entry, args=[
            'show', f'test/testfile/{fmt}_template-simple{ext}',
            *(('--silent',) if silent else ())
        ])

        assert result.exit_code == 0
        if silent:
            assert 'Cloning' not in result.stdout
            assert 'Downloading' not in result.stdout
            assert 'Unpacking' not in result.stdout
        else:
            assert 'Cloning' not in result.stdout
            assert 'Downloading' not in result.stdout
            assert 'Unpacking' in result.stdout

        assert 'Template: simple' in result.stdout
        assert 'Version: 0.0.1' in result.stdout
        assert 'Description: ' in result.stdout

    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    @pytest.mark.parametrize(
        ['fmt', 'ext', 'silent'],
        [
            ('7z', '.7z', True),
            ('rar', '.rar', False),
            ('bztar', '.tar.bz2', True),
            ('gztar', '.tar.gz', False),
            ('tar', '.tar', True),
            ('xztar', '.tar.xz', False),
            ('zip', '.zip', True),
        ]
    )
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    def test_download_file_not_unpack(self, fmt, ext, silent):
        runner = CliRunner()
        result = runner.invoke(cli_entry, args=[
            'show', get_testfile_url(f'{fmt}_template-simple{ext}'),
            *(('--silent',) if silent else ())
        ])

        assert result.exit_code == 0
        if silent:
            assert 'Cloning' not in result.stdout
            assert 'Downloading' not in result.stdout
            assert 'Unpacking' not in result.stdout
        else:
            assert 'Cloning' not in result.stdout
            assert 'Downloading' in result.stdout
            assert 'Unpacking' in result.stdout

        assert 'Template: simple' in result.stdout
        assert 'Version: 0.0.1' in result.stdout
        assert 'Description: ' in result.stdout
