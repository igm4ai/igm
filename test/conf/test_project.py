import os.path
from unittest import skipUnless

import pytest
from hbutils.testing import isolated_directory

from igm.conf.project import load_igm_project, IGMProject, NotIGMProject
from test.testings import TEMPLATE_SIMPLE_VERSION, TEMPLATE_TEST_VERSION


@pytest.mark.unittest
class TestConfProject:
    def test_load_igm_project_simple(self, simple_project):
        with load_igm_project(simple_project) as p:
            assert isinstance(p, IGMProject)
            assert p.name == 'hansbug-simple-demo'
            assert p.version == '0.3.2'
            assert p.template_name == 'simple'
            assert p.template_version == TEMPLATE_SIMPLE_VERSION

    def test_load_igm_project_simple_with_file(self, simple_project):
        with load_igm_project(os.path.join(simple_project, 'igmeta.py')) as p:
            assert isinstance(p, IGMProject)
            assert p.name == 'hansbug-simple-demo'
            assert p.version == '0.3.2'
            assert p.template_name == 'simple'
            assert p.template_version == TEMPLATE_SIMPLE_VERSION

    def test_load_igm_project_test(self, test_project):
        with load_igm_project(test_project) as p:
            assert isinstance(p, IGMProject)
            assert p.name == 'hansbug-demo'
            assert p.version == '0.3.2'
            assert p.template_name == 'test'
            assert p.template_version == TEMPLATE_TEST_VERSION

    @skipUnless(not os.path.exists('/not_found_dir'), 'directory not exist required')
    def test_load_igm_project_not_found(self):
        with pytest.raises(FileNotFoundError):
            with load_igm_project('/not_found_dir'):
                pytest.fail('Should not reach here!')

    def test_load_igm_project_invalid(self):
        with isolated_directory():
            with open('igmeta.py', 'w') as f:
                f.write("""
A = 1
                """)

            with pytest.raises(NotIGMProject):
                with load_igm_project('.'):
                    pytest.fail('Should not reach here!')

            with pytest.raises(NotIGMProject):
                with load_igm_project('igmeta.py'):
                    pytest.fail('Should not reach here!')
