import pytest
from hbutils.system import is_binary_file

from igm.utils import get_file_ext, splitext
from ..testings import get_testfile_path


@pytest.mark.unittest
class TestUtilsFile:
    @pytest.mark.parametrize(
        ['file', 'is_binary'],
        [
            ('zip_template-simple.zip', True),
            ('rar_template-simple.rar', True),
            ('xztar_template-simple.tar.xz', True),
            ('LICENSE', False),
            ('README.md', False),
        ]
    )
    def test_is_binary_file(self, file, is_binary):
        assert is_binary_file(get_testfile_path(file)) == is_binary

    @pytest.mark.parametrize(
        ['file', 'ext'],
        [
            ('zip_template-simple.zip', '.zip'),
            ('rar_template-simple.rar', '.rar'),
            ('xztar_template-simple.tar.xz', '.tar.xz'),
            ('LICENSE', ''),
            ('README.md', '.md'),
        ]
    )
    def test_get_file_ext(self, file, ext):
        assert get_file_ext(file) == ext

    @pytest.mark.parametrize(
        ['file', 'body', 'ext'],
        [
            ('zip_template-simple.zip', 'zip_template-simple', '.zip'),
            ('rar_template-simple.rar', 'rar_template-simple', '.rar'),
            ('xztar_template-simple.tar.xz', 'xztar_template-simple', '.tar.xz'),
            ('LICENSE', 'LICENSE', ''),
            ('README.md', 'README', '.md'),
        ]
    )
    def test_splitext(self, file, body, ext):
        assert splitext(file) == (body, ext)
