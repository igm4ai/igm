import os
from unittest import skipUnless

import pytest
from hbutils.testing import isolated_directory

from igm.utils import is_vcs_url, retrieve_from_vcs
from igm.utils.vcs import InvalidVCSURL
from ..testings import GITHUB_HOST


@pytest.mark.unittest
class TestUtilsVcs:
    def test_is_vcs_url(self):
        assert is_vcs_url(f'git+https://{GITHUB_HOST}/igm4ai/template-simple.git')
        assert is_vcs_url(f'svn+https://{GITHUB_HOST}/igm4ai/template-simple.git')
        assert is_vcs_url(f'git+ssh://git@{GITHUB_HOST}/igm4ai/template-simple.git')
        assert not is_vcs_url(f'https://{GITHUB_HOST}/igm4ai/template-simple.git')
        assert not is_vcs_url(f'file://{GITHUB_HOST}/igm4ai/template-simple.git')
        assert not is_vcs_url('jdsflkjsdlkfjdls')
        assert not is_vcs_url('/root')

    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    @skipUnless(not os.getenv('NO_GITHUB'), 'github not accessible')
    def test_retrieve_from_vcs(self):
        with isolated_directory({'template-simple': 'templates/simple'}):
            with pytest.raises(InvalidVCSURL):
                retrieve_from_vcs('/root', 'simple')

        with isolated_directory({'template-simple': 'templates/simple'}):
            retrieve_from_vcs(f'git+https://{GITHUB_HOST}/igm4ai/template-simple.git', 'simple')
            with open('simple/meta.py', 'r') as df, open('template-simple/meta.py', 'r') as of:
                assert df.read() == of.read()
