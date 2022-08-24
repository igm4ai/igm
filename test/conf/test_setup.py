import pytest

from igm.conf import load_igm_setup
from igm.template import IGMTemplate
from test.testings import TEMPLATE_SIMPLE, TEMPLATE_SIMPLE_FILE, GITHUB_HOST


@pytest.mark.unittest
class TestDistSetup:
    def test_load_igm_setup_local(self):
        with pytest.raises(FileNotFoundError):
            with load_igm_setup('/a/path/not/exist'):
                pytest.fail('Should not reach here.')

        with load_igm_setup(TEMPLATE_SIMPLE) as template:
            assert isinstance(template, IGMTemplate)
            assert template.name == 'simple'
            assert template.version == '0.0.1'
            assert template.description == 'This is a simplest IGM template'

        with load_igm_setup(TEMPLATE_SIMPLE_FILE) as template:
            assert isinstance(template, IGMTemplate)
            assert template.name == 'simple'
            assert template.version == '0.0.1'
            assert template.description == 'This is a simplest IGM template'

    def test_load_igm_setup_github(self):
        with load_igm_setup(f'git+https://{GITHUB_HOST}/igm4ai/template-simple.git') as template:
            assert isinstance(template, IGMTemplate)
            assert template.name == 'simple'
            assert template.version == '0.0.1'
            assert template.description == 'This is a simplest IGM template'

    def test_load_igm_setup_download(self):
        with load_igm_setup('https://codeload.github.com/igm4ai/template-simple/zip/refs/heads/main',
                            'template-simple-main') as template:
            assert isinstance(template, IGMTemplate)
            assert template.name == 'simple'
            assert template.version == '0.0.1'
            assert template.description == 'This is a simplest IGM template'
