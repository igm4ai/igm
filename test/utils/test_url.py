import pytest

from igm.utils import get_url_filename, get_url_ext
from ..testings import get_testfile_url


@pytest.mark.unittest
class TestUtilsUrl:
    def test_get_url_filename(self):
        assert get_url_filename(get_testfile_url('sdjlk873jdf%20.file')) == 'sdjlk873jdf .file'
        assert get_url_filename(get_testfile_url('sdjlk873jdf%20.file'), 'application/pdf') \
               == 'sdjlk873jdf .file.pdf'
        assert get_url_filename(get_testfile_url('sdjlk873jdf%20.pdf'), 'application/pdf') \
               == 'sdjlk873jdf .pdf'

    def test_get_url_ext(self):
        assert get_url_ext(get_testfile_url('sdjlk873jdf%20.file')) == '.file'
        assert get_url_ext(get_testfile_url('sdjlk873jdf%20.tar.gz')) == '.tar.gz'
        assert get_url_ext(get_testfile_url('sdjlk873jdf%20.tar.gz'), 'application/pdf') == '.pdf'
