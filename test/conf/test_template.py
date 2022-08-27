import io
import os.path
from textwrap import dedent

import pytest
from hbutils.testing import capture_output

from igm.conf import IGMTemplate
from igm.utils import normpath
from ..testings import assert_same_path


@pytest.mark.unittest
class TestConfTemplate:
    def test_igm_template_base(self):
        template = IGMTemplate('mt', '0.5.4', 'My Template', os.path.join('test', 'utils'))
        assert template.name == 'mt'
        assert template.version == '0.5.4'
        assert template.description == 'My Template'

        assert_same_path(template.path, os.path.join('test', 'utils'))
        assert template.template_dir == 'template'

        with capture_output() as c:
            template.print_info()
        assert c.stdout.strip() == dedent(f"""
mt, v0.5.4
My Template
Located at {normpath('test/utils')!r}.
        """.strip())

        with io.StringIO() as sf:
            template.print_info(sf)
            assert sf.getvalue().strip() == dedent(f"""
mt, v0.5.4
My Template
Located at {normpath('test/utils')!r}.
            """.strip())

        assert repr(template) == '<IGMTemplate mt, v0.5.4>'
