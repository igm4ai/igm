import pytest

from igm.conf import load_igm_setup
from igm.template import IGMTemplate
from test.testings import TEMPLATE_SIMPLE, TEMPLATE_SIMPLE_FILE, GITHUB_HOST


@pytest.mark.unittest
class TestDistSetup:
    def test_load_igm_setup_local(self):
        with pytest.raises(FileNotFoundError):
            load_igm_setup('/a/path/not/exist')

        template = load_igm_setup(TEMPLATE_SIMPLE)
        assert isinstance(template, IGMTemplate)
        assert template.name == 'simple'
        assert template.version == '0.0.1'
        assert template.description == 'This is a simplest IGM template'

        template = load_igm_setup(TEMPLATE_SIMPLE_FILE)
        assert isinstance(template, IGMTemplate)
        assert template.name == 'simple'
        assert template.version == '0.0.1'
        assert template.description == 'This is a simplest IGM template'

    def test_load_igm_setup_github(self):
        template = load_igm_setup(f'git+https://{GITHUB_HOST}/igm4ai/template-simple.git')
        assert isinstance(template, IGMTemplate)
        assert template.name == 'simple'
        assert template.version == '0.0.1'
        assert template.description == 'This is a simplest IGM template'
