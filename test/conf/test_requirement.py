import platform
from subprocess import CalledProcessError

import pytest
from hbutils.testing import isolated_directory, capture_output, disable_output

from igm.conf.requirement import load_req, pip, check_req


@pytest.mark.unittest
class TestConfRequirement:
    def test_load_req(self):
        with isolated_directory({'requirements.txt': 'test/testfile/requirements-test.txt'}):
            assert load_req('requirements.txt') == [
                'pytest<=6.2.5,>=2.8.0',
                'pytest-cov',
                'pytest-httpbin==1.0.0',
                'pytest-mock==2.0.0',
                'httpbin==0.7.0',
                'trustme',
                'wheel',
                'Flask<2.0,>1.0',
                'markupsafe<2.1',
            ]

    def test_pip_v(self):
        with capture_output() as co:
            pip('-V')

        major, minor, *_ = platform.python_version_tuple()
        ver = f'{major}.{minor}'
        assert ver in co.stdout
        assert 'pip' in co.stdout

    def test_pip_invalid(self):
        with pytest.raises(CalledProcessError):
            with disable_output():
                _ = pip('-FJkldfjslk')

    def test_check_req(self):
        assert not check_req(['not_exist_package==3.2.1'])
        assert check_req(['hbutils>=0.7.0', 'easydict'])
