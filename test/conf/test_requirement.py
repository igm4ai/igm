import platform
from subprocess import CalledProcessError

import pytest
from hbutils.testing import isolated_directory

from igm.conf.requirement import load_req, pip


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
        exitcode, stdout, stderr = pip('-V', capture_output=True)
        assert exitcode == 0

        major, minor, *_ = platform.python_version_tuple()
        ver = f'{major}.{minor}'
        assert ver in stdout
        assert 'pip' in stdout

    def test_pip_v_no_capture(self):
        exitcode, stdout, stderr = pip('-V')
        assert exitcode == 0
        assert stdout is None
        assert stderr is None

    def test_pip_invalid(self):
        with pytest.raises(CalledProcessError):
            _ = pip('-FJkldfjslk', capture_output=True)
