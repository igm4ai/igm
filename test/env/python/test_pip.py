import pytest
from hbutils.system import package_version

from igm.env.python import Pip


@pytest.mark.unittest
class TestEnvPythonPip:
    def test_pip_actual(self):
        pip = Pip()
        assert pip.version == package_version('pip')
        assert pip('hbutils').name == 'hbutils'
        assert pip('hbutils').version == package_version('hbutils')

        assert str(pip) == f'<Pip version: {package_version("pip")}>'
        assert repr(pip) == f'<Pip version: {package_version("pip")}>'

        assert str(pip('hbutils')) == f'hbutils=={package_version("hbutils")}'
        assert repr(pip('hbutils')) == f'<PipPackage hbutils, version: {package_version("hbutils")}>'

    def test_pip_version(self, pip_19_2_3):
        pip = Pip()
        assert pip.version == '19.2.3'
        assert pip('hbutils').name == 'hbutils'
        assert pip('hbutils').version == package_version('hbutils')

        assert str(pip) == '<Pip version: 19.2.3>'
        assert repr(pip) == '<Pip version: 19.2.3>'

        assert str(pip('hbutils')) == f'hbutils=={package_version("hbutils")}'
        assert repr(pip('hbutils')) == f'<PipPackage hbutils, version: {package_version("hbutils")}>'

    def test_inner_pip_version(self, pip_19_2_3, hbutils_7_9_10):
        pip = Pip()
        assert pip.version == '19.2.3'
        assert pip('hbutils').name == 'hbutils'
        assert pip('hbutils').version == '7.9.10'

        assert str(pip) == '<Pip version: 19.2.3>'
        assert repr(pip) == '<Pip version: 19.2.3>'

        assert str(pip('hbutils')) == f'hbutils==7.9.10'
        assert repr(pip('hbutils')) == f'<PipPackage hbutils, version: 7.9.10>'
