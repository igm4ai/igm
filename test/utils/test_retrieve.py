import os.path
import pathlib
import shutil

import pytest
from hbutils.testing import isolated_directory

from igm.utils import retrieve
from test.testings import GITHUB_HOST


@pytest.mark.unittest
class TestUtilsRetrieve:
    @pytest.mark.parametrize(['fmt'], [('7z',), ('rar',)])
    def test_retrieve_7z_rar(self, fmt):
        with retrieve(f'test/testfile/{fmt}_template-simple.{fmt}') as fd:
            assert os.path.exists(fd)
            assert os.path.isdir(fd)
            assert os.path.exists(os.path.join(fd, 'meta.py'))
            assert os.path.exists(os.path.join(fd, 'README.md'))
            assert 'igm.conf' in pathlib.Path(os.path.join(fd, 'meta.py')).read_text()

    @pytest.mark.parametrize(['fmt'], [('7z',), ('rar',)])
    def test_retrieve_not_unpack_7z_rar(self, fmt):
        with retrieve(f'test/testfile/{fmt}_template-simple.{fmt}', auto_unpack=False) as fd:
            assert os.path.exists(fd)
            assert os.path.isfile(fd)
            _, filename = os.path.split(fd)
            assert filename == f'{fmt}_template-simple.{fmt}'

    @pytest.mark.parametrize(
        ['fmt', 'exts'],
        [
            ('bztar', ['.tar.bz2', '.tbz2']),
            ('gztar', ['.tar.gz', '.tgz']),
            ('tar', ['.tar']),
            ('xztar', ['.tar.xz', '.txz']),
            ('zip', ['.zip']),
        ]
    )
    def test_retrieve_common_archive(self, fmt, exts):
        with isolated_directory({'template-simple': 'templates/simple'}):
            product = shutil.make_archive('template-simple-zip', fmt, 'template-simple')

            with retrieve(product) as fd:
                assert os.path.exists(fd)
                assert os.path.isdir(fd)
                assert os.path.exists(os.path.join(fd, 'meta.py'))
                assert os.path.exists(os.path.join(fd, 'README.md'))
                assert pathlib.Path('template-simple/meta.py').read_text() == \
                       pathlib.Path(os.path.join(fd, 'meta.py')).read_text()

    @pytest.mark.parametrize(
        ['fmt', 'exts'],
        [
            ('bztar', ['.tar.bz2', '.tbz2']),
            ('gztar', ['.tar.gz', '.tgz']),
            ('tar', ['.tar']),
            ('xztar', ['.tar.xz', '.txz']),
            ('zip', ['.zip']),
        ]
    )
    def test_retrieve_common_archive_not_unpack(self, fmt, exts):
        with isolated_directory({'template-simple': 'templates/simple'}):
            product = shutil.make_archive('template-simple-zip', fmt, 'template-simple')
            _, pfilename = os.path.split(product)

            with retrieve(product, auto_unpack=False) as fd:
                assert os.path.exists(fd)
                assert os.path.isfile(fd)
                _, filename = os.path.split(fd)
                assert filename == pfilename

    def test_retrieve_path(self):
        with isolated_directory({'template-simple': 'templates/simple'}):
            with retrieve('template-simple') as fd:
                assert os.path.exists(fd)
                assert os.path.isdir(fd)
                assert os.path.exists(os.path.join(fd, 'meta.py'))
                assert os.path.exists(os.path.join(fd, 'README.md'))

    @pytest.mark.parametrize(['fmt'], [('7z',), ('rar',)])
    def test_download_file(self, fmt):
        with isolated_directory():
            with retrieve(f'https://{GITHUB_HOST}/igm4ai/igm-testfile/raw/main/{fmt}_template-simple.{fmt}') as fd:
                assert os.path.exists(fd)
                assert os.path.isdir(fd)
                assert os.path.exists(os.path.join(fd, 'meta.py'))
                assert os.path.exists(os.path.join(fd, 'README.md'))
                assert 'igm.conf' in pathlib.Path(os.path.join(fd, 'meta.py')).read_text()

    @pytest.mark.parametrize(['fmt'], [('7z',), ('rar',)])
    def test_download_file_not_unpack(self, fmt):
        with isolated_directory():
            with retrieve(f'https://{GITHUB_HOST}/igm4ai/igm-testfile/raw/main/{fmt}_template-simple.{fmt}',
                          auto_unpack=False) as fd:
                assert os.path.exists(fd)
                assert os.path.isfile(fd)
                _, filename = os.path.split(fd)
                assert filename == f'{fmt}_template-simple.{fmt}'

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
            with pytest.raises(FileNotFoundError):
                with retrieve(f'ffffffff://{GITHUB_HOST}/igm4ai/template-simple.git'):
                    pytest.fail('Should not reach here.')
