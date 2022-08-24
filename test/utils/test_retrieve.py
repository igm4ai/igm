import os.path
import pathlib

import pytest
from hbutils.testing import isolated_directory

from igm.utils import retrieve
from test.testings import GITHUB_HOST


@pytest.mark.unittest
class TestUtilsRetrieve:
    @pytest.mark.parametrize(
        ['fmt', 'ext'],
        [
            ('7z', '.7z'),
            ('rar', '.rar'),
            ('bztar', '.tar.bz2'),
            ('gztar', '.tar.gz'),
            ('tar', '.tar'),
            ('xztar', '.tar.xz'),
            ('zip', '.zip'),
        ]
    )
    def test_retrieve_local_archive(self, fmt, ext):
        with retrieve(f'test/testfile/{fmt}_template-simple{ext}') as fd:
            assert os.path.exists(fd)
            assert os.path.isdir(fd)
            assert os.path.exists(os.path.join(fd, 'meta.py'))
            assert os.path.exists(os.path.join(fd, 'README.md'))
            assert 'igm.conf' in pathlib.Path(os.path.join(fd, 'meta.py')).read_text()

    @pytest.mark.parametrize(
        ['fmt', 'ext'],
        [
            ('7z', '.7z'),
            ('rar', '.rar'),
            ('bztar', '.tar.bz2'),
            ('gztar', '.tar.gz'),
            ('tar', '.tar'),
            ('xztar', '.tar.xz'),
            ('zip', '.zip'),
        ]
    )
    def test_retrieve_local_archive_not_unpack(self, fmt, ext):
        with retrieve(f'test/testfile/{fmt}_template-simple{ext}', auto_unpack=False) as fd:
            assert os.path.exists(fd)
            assert os.path.isfile(fd)
            _, filename = os.path.split(fd)
            assert filename == f'{fmt}_template-simple{ext}'

    def test_retrieve_path(self):
        with isolated_directory({'template-simple': 'templates/simple'}):
            with retrieve('template-simple') as fd:
                assert os.path.exists(fd)
                assert os.path.isdir(fd)
                assert os.path.exists(os.path.join(fd, 'meta.py'))
                assert os.path.exists(os.path.join(fd, 'README.md'))

    @pytest.mark.parametrize(
        ['fmt', 'ext'],
        [
            ('7z', '.7z'),
            ('rar', '.rar'),
            ('bztar', '.tar.bz2'),
            ('gztar', '.tar.gz'),
            ('tar', '.tar'),
            ('xztar', '.tar.xz'),
            ('zip', '.zip'),
        ]
    )
    def test_download_file(self, fmt, ext):
        with isolated_directory():
            with retrieve(f'https://{GITHUB_HOST}/igm4ai/igm-testfile/raw/main/{fmt}_template-simple{ext}') as fd:
                assert os.path.exists(fd)
                assert os.path.isdir(fd)
                assert os.path.exists(os.path.join(fd, 'meta.py'))
                assert os.path.exists(os.path.join(fd, 'README.md'))
                assert 'igm.conf' in pathlib.Path(os.path.join(fd, 'meta.py')).read_text()

    @pytest.mark.parametrize(
        ['fmt', 'ext'],
        [
            ('7z', '.7z'),
            ('rar', '.rar'),
            ('bztar', '.tar.bz2'),
            ('gztar', '.tar.gz'),
            ('tar', '.tar'),
            ('xztar', '.tar.xz'),
            ('zip', '.zip'),
        ]
    )
    def test_download_file_not_unpack(self, fmt, ext):
        with isolated_directory():
            with retrieve(f'https://{GITHUB_HOST}/igm4ai/igm-testfile/raw/main/{fmt}_template-simple{ext}',
                          auto_unpack=False) as fd:
                assert os.path.exists(fd)
                assert os.path.isfile(fd)
                _, filename = os.path.split(fd)
                assert filename == f'{fmt}_template-simple{ext}'

    def test_download_file_with_content_type(self):
        with isolated_directory():
            with retrieve('https://codeload.github.com/igm4ai/template-simple/zip/refs/heads/main') as fd:
                assert os.path.exists(fd)
                assert os.path.isdir(fd)
                assert os.path.exists(os.path.join(fd, 'template-simple-main', 'meta.py'))
                assert os.path.exists(os.path.join(fd, 'template-simple-main', 'README.md'))
                assert 'igm.conf' in pathlib.Path(os.path.join(fd, 'template-simple-main', 'meta.py')).read_text()

    def test_retrieve_from_github(self):
        with isolated_directory():
            with retrieve(f'git+https://{GITHUB_HOST}/igm4ai/template-simple.git') as fd:
                assert os.path.exists(fd)
                assert os.path.isdir(fd)
                assert os.path.exists(os.path.join(fd, 'meta.py'))
                assert os.path.exists(os.path.join(fd, 'README.md'))
                assert 'igm.conf' in pathlib.Path(os.path.join(fd, 'meta.py')).read_text()

    def test_invalid_scheme(self):
        with isolated_directory():
            with pytest.raises((FileNotFoundError, OSError)):
                with retrieve(f'ffffffff://{GITHUB_HOST}/igm4ai/template-simple.git'):
                    pytest.fail('Should not reach here.')
