import os.path
import pathlib
from unittest import skipUnless

import pytest
from hbutils.testing import isolated_directory, capture_output

from igm.utils import retrieve
from ..testings import GITHUB_HOST, get_testfile_url, TEMPLATE_SIMPLE_REPO_GIT


@pytest.mark.unittest
class TestUtilsRetrieve:
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
    def test_retrieve_local_archive(self, fmt, ext, silent):
        with capture_output() as co:
            with retrieve(f'test/testfile/{fmt}_template-simple{ext}', silent=silent) as fd:
                assert os.path.exists(fd)
                assert os.path.isdir(fd)
                assert os.path.exists(os.path.join(fd, 'meta.py'))
                assert os.path.exists(os.path.join(fd, 'README.md'))
                assert 'igm.conf' in pathlib.Path(os.path.join(fd, 'meta.py')).read_text()

        if not silent:
            assert co.stdout.strip()
            assert 'Unpacking archive' in co.stdout
        else:
            assert not co.stdout.strip()

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
    def test_retrieve_local_archive_not_unpack(self, fmt, ext, silent):
        with capture_output() as co:
            with retrieve(f'test/testfile/{fmt}_template-simple{ext}', auto_unpack=False, silent=silent) as fd:
                assert os.path.exists(fd)
                assert os.path.isfile(fd)
                _, filename = os.path.split(fd)
                assert filename == f'{fmt}_template-simple{ext}'

        assert not co.stdout.strip()

    def test_retrieve_path(self):
        with isolated_directory({'template-simple': 'templates/simple'}):
            with retrieve('template-simple') as fd:
                assert os.path.exists(fd)
                assert os.path.isdir(fd)
                assert os.path.exists(os.path.join(fd, 'meta.py'))
                assert os.path.exists(os.path.join(fd, 'README.md'))

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
    def test_download_file(self, fmt, ext, silent):
        with capture_output() as co:
            with isolated_directory():
                with retrieve(get_testfile_url(f'{fmt}_template-simple{ext}'), silent=silent) as fd:
                    assert os.path.exists(fd)
                    assert os.path.isdir(fd)
                    assert os.path.exists(os.path.join(fd, 'meta.py'))
                    assert os.path.exists(os.path.join(fd, 'README.md'))
                    assert 'igm.conf' in pathlib.Path(os.path.join(fd, 'meta.py')).read_text()

        if not silent:
            assert co.stdout.strip()
            assert 'Downloading' in co.stdout
            assert 'Unpacking archive' in co.stdout
        else:
            assert not co.stdout.strip()

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
        with capture_output() as co:
            with isolated_directory():
                with retrieve(get_testfile_url(f'{fmt}_template-simple{ext}'), auto_unpack=False, silent=silent) as fd:
                    assert os.path.exists(fd)
                    assert os.path.isfile(fd)
                    _, filename = os.path.split(fd)
                    assert filename == f'{fmt}_template-simple{ext}'

        if not silent:
            assert co.stdout.strip()
            assert 'Downloading' in co.stdout
            assert 'Unpacking archive' not in co.stdout
        else:
            assert not co.stdout.strip()

    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    @skipUnless(not os.getenv('NO_GITHUB'), 'github not accessible')
    def test_download_file_with_content_type(self):
        with isolated_directory():
            with retrieve('https://codeload.github.com/igm4ai/template-simple/zip/refs/heads/main', silent=True) as fd:
                assert os.path.exists(fd)
                assert os.path.isdir(fd)
                assert os.path.exists(os.path.join(fd, 'template-simple-main', 'meta.py'))
                assert os.path.exists(os.path.join(fd, 'template-simple-main', 'README.md'))
                assert 'igm.conf' in pathlib.Path(os.path.join(fd, 'template-simple-main', 'meta.py')).read_text()

    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    def test_retrieve_from_github(self):
        with capture_output() as co:
            with isolated_directory():
                with retrieve(TEMPLATE_SIMPLE_REPO_GIT) as fd:
                    assert os.path.exists(fd)
                    assert os.path.isdir(fd)
                    assert os.path.exists(os.path.join(fd, 'meta.py'))
                    assert os.path.exists(os.path.join(fd, 'README.md'))
                    assert 'igm.conf' in pathlib.Path(os.path.join(fd, 'meta.py')).read_text()

        assert 'Cloning from VCS' in co.stdout

    def test_invalid_scheme(self):
        with isolated_directory():
            with pytest.raises((FileNotFoundError, OSError)):
                with retrieve(f'ffffffff://{GITHUB_HOST}/igm4ai/template-simple.git'):
                    pytest.fail('Should not reach here.')
