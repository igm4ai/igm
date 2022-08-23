import os.path
import pathlib
import shutil

import pytest
from hbutils.testing import isolated_directory
from mock import patch

from igm.utils import unpack_archive
from igm.utils.archive import SevenZipExtractionNotSupported, RARExtractionNotSupported


@pytest.mark.unittest
class TestUtilsArchive:
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
    def test_unpack_archive_common(self, fmt, exts):
        with isolated_directory({'template-simple': 'templates/simple'}):
            product = shutil.make_archive('template-simple-zip', fmt, 'template-simple')
            os.path.normcase(product)
            assert any([product.endswith(ext) for ext in exts]), \
                f'Invalid extension of file {product!r}, but {exts!r} expected.'

            unpack_archive(product, 'decompressed')
            assert pathlib.Path('template-simple/meta.py').read_text() == \
                   pathlib.Path('decompressed/meta.py').read_text()

    def test_unpack_archive_7z(self):
        with isolated_directory({'testfile': 'test/testfile'}):
            unpack_archive('testfile/7z_template-simple.7z', 'decompressed')
            assert 'igm.conf' in pathlib.Path('decompressed/meta.py').read_text()

    @patch('igm.utils.archive.py7zr', None)
    def test_unpack_archive_7z_without_installation(self):
        with isolated_directory({'testfile': 'test/testfile'}):
            with pytest.raises(SevenZipExtractionNotSupported):
                unpack_archive('testfile/7z_template-simple.7z', 'decompressed')

    def test_unpack_archive_rar(self):
        with isolated_directory({'testfile': 'test/testfile'}):
            unpack_archive('testfile/rar_template-simple.rar', 'decompressed')
            assert 'igm.conf' in pathlib.Path('decompressed/meta.py').read_text()

    @patch('igm.utils.archive.rarfile', None)
    def test_unpack_archive_rar_without_installation(self):
        with isolated_directory({'testfile': 'test/testfile'}):
            with pytest.raises(RARExtractionNotSupported):
                unpack_archive('testfile/7z_template-simple.rar', 'decompressed')
