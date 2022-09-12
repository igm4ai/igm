import io
import os.path
from textwrap import dedent
from unittest.mock import patch

import pytest
from hbutils.testing import capture_output, isolated_directory

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
        assert_same_path(template.template_dir, os.path.join(template.path, 'template'))

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

    def test_template_run(self, test_template):
        with isolated_directory():
            test_template.run('project', silent=True)

            assert os.path.exists('project')
            assert os.path.isdir('project')
            assert os.path.exists('project/README.md')
            assert os.path.exists('project/igmeta.py')

    def test_template_run_error(self, test_template):
        with isolated_directory(), patch.dict('os.environ', {'MAKE_ERROR': '1'}, clear=False):
            with pytest.raises(ValueError):
                test_template.run('project', silent=True)

    def test_template_run_exists(self, test_template):
        with isolated_directory():
            os.makedirs('project', exist_ok=True)
            with pytest.raises(FileExistsError):
                test_template.run('project', silent=True)
