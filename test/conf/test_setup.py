import pytest

from igm.conf import load_igm_setup
from igm.template import IGMTemplate
from test.testings import TEMPLATE_SIMPLE, assert_same_path, TEMPLATE_SIMPLE_FILE


@pytest.mark.unittest
class TestDistSetup:
    def test_load_igm_setup(self):
        with pytest.raises(FileNotFoundError):
            load_igm_setup('/a/path/not/exist')

        template = load_igm_setup(TEMPLATE_SIMPLE)
        assert isinstance(template, IGMTemplate)
        assert template.title == 'simple'
        assert template.version == '0.0.1'
        assert template.description == 'This is a simplest IGM template'
        assert_same_path(template.path, TEMPLATE_SIMPLE)

        template = load_igm_setup(TEMPLATE_SIMPLE_FILE)
        assert isinstance(template, IGMTemplate)
        assert template.title == 'simple'
        assert template.version == '0.0.1'
        assert template.description == 'This is a simplest IGM template'
        assert_same_path(template.path, TEMPLATE_SIMPLE)
