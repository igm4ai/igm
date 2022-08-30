import os
from unittest import skipUnless

import pytest

from igm.conf import load_igm_setup, IGMTemplate
from ..testings import TEMPLATE_SIMPLE, TEMPLATE_SIMPLE_FILE, TEMPLATE_SIMPLE_VERSION, TEMPLATE_LINEAR, \
    TEMPLATE_LINEAR_VERSION, TEMPLATE_SIMPLE_REPO_GIT


@pytest.mark.unittest
class TestConfSetup:
    def test_load_igm_setup_local(self):
        with pytest.raises(FileNotFoundError):
            with load_igm_setup('/a/path/not/exist'):
                pytest.fail('Should not reach here.')

        with load_igm_setup(TEMPLATE_SIMPLE) as template:
            assert isinstance(template, IGMTemplate)
            assert template.name == 'simple'
            assert template.version == TEMPLATE_SIMPLE_VERSION
            assert template.description == 'This is a simplest IGM template'

        with load_igm_setup(TEMPLATE_SIMPLE_FILE) as template:
            assert isinstance(template, IGMTemplate)
            assert template.name == 'simple'
            assert template.version == TEMPLATE_SIMPLE_VERSION
            assert template.description == 'This is a simplest IGM template'

    @skipUnless(not os.getenv('NO_INTERNET'), 'no internet required')
    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    def test_load_igm_setup_github(self):
        with load_igm_setup(TEMPLATE_SIMPLE_REPO_GIT) as template:
            assert isinstance(template, IGMTemplate)
            assert template.name == 'simple'
            assert template.version == TEMPLATE_SIMPLE_VERSION
            assert template.description == 'This is a simplest IGM template'

    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    @skipUnless(not os.getenv('NO_GITHUB'), 'github not accessible')
    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    def test_load_igm_setup_download(self):
        with load_igm_setup('https://codeload.github.com/igm4ai/template-simple/zip/refs/heads/main',
                            'template-simple-main') as template:
            assert isinstance(template, IGMTemplate)
            assert template.name == 'simple'
            assert template.version == TEMPLATE_SIMPLE_VERSION
            assert template.description == 'This is a simplest IGM template'

    def test_load_linear_regression(self):
        with load_igm_setup(TEMPLATE_LINEAR) as template:
            assert isinstance(template, IGMTemplate)
            assert template.name == 'linear-regression'
            assert template.version == TEMPLATE_LINEAR_VERSION
            assert template.description == 'This is a IGM template for linear regression problem'
