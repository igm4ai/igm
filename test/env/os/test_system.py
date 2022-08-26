from unittest import skipUnless

import pytest
from hbutils.system import is_windows, is_linux, is_macos

from igm.env.os import OS, get_os_info


@pytest.mark.unittest
class TestEnvOsSystem:
    def test_os_with_linux_machine_1(self, linux_machine_1):
        os = OS(get_os_info())
        assert os.type == 'linux'
        assert os.release == '5.15.0-46-generic'
        assert os.version == '#49~20.04.1-Ubuntu SMP Thu Aug 4 19:15:44 UTC 2022'
        assert os.node == 'hansbug-MS-7C94'

        assert str(os) == '<OS Linux, #49~20.04.1-Ubuntu SMP Thu Aug 4 19:15:44 UTC 2022, node: \'hansbug-MS-7C94\'>'
        assert repr(os) == '<OS Linux, #49~20.04.1-Ubuntu SMP Thu Aug 4 19:15:44 UTC 2022, node: \'hansbug-MS-7C94\'>'

    def test_os_with_window_machine_1(self, windows_machine_1):
        os = OS(get_os_info())
        assert os.type == 'win'
        assert os.release == '10'
        assert os.version == '10.0.19041'
        assert os.node == 'LAPTOP-37QSG5BO'

        assert str(os) == '<OS Windows, 10.0.19041, node: \'LAPTOP-37QSG5BO\'>'
        assert repr(os) == '<OS Windows, 10.0.19041, node: \'LAPTOP-37QSG5BO\'>'

    @skipUnless(is_windows(), 'windows only')
    def test_os_actual_on_windows(self):
        os = OS(get_os_info())
        assert os.type == 'win'

    @skipUnless(is_linux(), 'linux only')
    def test_os_actual_on_linux(self):
        os = OS(get_os_info())
        assert os.type == 'linux'

    @skipUnless(is_macos(), 'macos only')
    def test_os_actual_on_macos(self):
        os = OS(get_os_info())
        assert os.type == 'mac'
