import pytest

from igm.env.os import OSType


@pytest.mark.unittest
class TestEnvOsType:
    def test_loads(self):
        assert OSType.loads('linux') == OSType.LINUX
        assert OSType.loads('Linux') == OSType.LINUX
        assert OSType.loads('LINUX') == OSType.LINUX

        assert OSType.loads('win') == OSType.WINDOWS
        assert OSType.loads('Windows') == OSType.WINDOWS
        assert OSType.loads('WINDOWS') == OSType.WINDOWS

        assert OSType.loads('mac') == OSType.DARWIN
        assert OSType.loads('macos') == OSType.DARWIN
        assert OSType.loads('darwin') == OSType.DARWIN

        assert OSType.loads('java') == OSType.JAVA
        assert OSType.loads('Java') == OSType.JAVA
        assert OSType.loads('JAVA') == OSType.JAVA

        with pytest.raises(KeyError):
            _ = OSType.loads('skdfjlskfdj')
        with pytest.raises(TypeError):
            _ = OSType.loads(None)

    def test_str(self):
        assert str(OSType.LINUX) == 'Linux'
        assert str(OSType.WINDOWS) == 'Windows'
        assert str(OSType.DARWIN) == 'macOS'
        assert str(OSType.JAVA) == 'Java'

    def test_repr(self):
        assert repr(OSType.LINUX) == '<OSType Linux>'
        assert repr(OSType.WINDOWS) == '<OSType Windows>'
        assert repr(OSType.DARWIN) == '<OSType macOS>'
        assert repr(OSType.JAVA) == '<OSType Java>'

    def test_eq(self):
        assert OSType.LINUX == OSType.LINUX
        assert OSType.LINUX == 'linux'
        assert OSType.LINUX == 'Linux'
        assert OSType.LINUX == 'LINUX'
        assert OSType.LINUX != OSType.WINDOWS
        assert OSType.LINUX != 'wtf'
        assert OSType.LINUX != 2

        assert OSType.WINDOWS == OSType.WINDOWS
        assert OSType.WINDOWS == 'windows'
        assert OSType.WINDOWS == 'Windows'
        assert OSType.WINDOWS == 'win'
        assert OSType.WINDOWS != OSType.DARWIN
        assert OSType.WINDOWS != 'wtf'
        assert OSType.WINDOWS != 2

        assert OSType.DARWIN == OSType.DARWIN
        assert OSType.DARWIN == 'darwin'
        assert OSType.DARWIN == 'Darwin'
        assert OSType.DARWIN == 'macOS'
        assert OSType.DARWIN == 'MACOS'
        assert OSType.DARWIN == 'mac'
        assert OSType.DARWIN == 'MAC'
        assert OSType.DARWIN != OSType.JAVA
        assert OSType.DARWIN != 'wtf'
        assert OSType.DARWIN != 2

        assert OSType.JAVA == OSType.JAVA
        assert OSType.JAVA == 'java'
        assert OSType.JAVA == 'Java'
        assert OSType.JAVA == 'JAVA'
        assert OSType.JAVA != OSType.WINDOWS
        assert OSType.JAVA != 'wtf'
        assert OSType.JAVA != 2
