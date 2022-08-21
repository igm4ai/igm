import pytest

from igm.conf import load_igm_setup
from igm.template import IGMTemplate
from test.testings import TEMPLATE_SIMPLE


@pytest.mark.unittest
class TestDistSetup:
    def test_load_igm_setup(self):
        with pytest.raises(FileNotFoundError):
            load_igm_setup('/a/path/not/exist')

        template = load_igm_setup(TEMPLATE_SIMPLE)
        assert isinstance(template, IGMTemplate)
