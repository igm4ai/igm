import os
import platform
from unittest import skipUnless
from unittest.mock import patch, MagicMock

import psutil
import pytest
from hbutils.system import which, is_windows, is_linux, is_macos, package_version

from igm.env import sys
from igm.env.internet.net import CONNECT_CACHE_TTL
from ..testings import ONE_GPU_1_DATA, CPU_INFO_1, CPU_INFO_100, MEMORY_INFO_100


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestEnvSystem:
    @patch('igm.env.system.get_nvidia_info', MagicMock(return_value=ONE_GPU_1_DATA))
    def test_cuda(self):
        assert sys.cuda
        assert sys.cuda.version == '11.4'
        assert sys.cuda.driver_version == '470.141.3'

    @patch('igm.env.hardware.nvidia.which', MagicMock(return_value=None))
    def test_no_cuda(self):
        assert sys.cuda is None

    @patch('igm.env.system.get_nvidia_info', MagicMock(return_value=ONE_GPU_1_DATA))
    def test_gpu(self):
        assert sys.gpu
        assert sys.gpu.num == 1
        assert sys.gpu[0].name == 'NVIDIA GeForce RTX 2060'
        assert sys.gpu[0].memory.total == 12604932096

    @patch('igm.env.hardware.nvidia.which', MagicMock(return_value=None))
    def test_no_gpu(self):
        assert not sys.gpu

    @skipUnless(which('nvidia-smi'), 'nvidia-smi cli required')
    def test_cuda_actual(self):
        assert sys.cuda
        assert sys.cuda.version > '8'
        assert sys.cuda.version < 20

    @skipUnless(not which('nvidia-smi'), 'no nvidia-smi cli required')
    def test_no_cuda_actual(self):
        assert not sys.cuda

    @skipUnless(which('nvidia-smi'), 'nvidia-smi cli required')
    def test_gpu_actual(self):
        assert sys.gpu
        assert sys.gpu.num >= 1

    @skipUnless(not which('nvidia-smi'), 'no nvidia-smi cli required')
    def test_no_gpu_actual(self):
        assert not sys.gpu

    @patch('igm.env.system.get_cpu_info', MagicMock(return_value=CPU_INFO_1))
    def test_cpu_1(self):
        assert sys.cpu
        assert sys.cpu.num == 6
        assert sys.cpu.brand == 'Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz'
        assert sys.cpu.arch == 'x86_64'
        assert sys.cpu.usage.ratio == pytest.approx(0.20016666666666666)

    @patch('igm.env.system.get_cpu_info', MagicMock(return_value=CPU_INFO_100))
    def test_cpu_100(self):
        assert sys.cpu
        assert sys.cpu.num == 112
        assert sys.cpu.brand == 'Intel(R) Xeon(R) Gold 6348 CPU @ 2.60GHz'
        assert sys.cpu.arch == 'x86_64'
        assert sys.cpu.usage.ratio == pytest.approx(0.015669642857142858)

    def test_cpu_actual(self):
        assert sys.cpu
        assert sys.cpu.num == os.cpu_count()

    @patch('igm.env.system.get_memory_info', MagicMock(return_value=MEMORY_INFO_100))
    def test_memory(self):
        assert sys.memory
        assert sys.memory.total == 1013991469056
        assert sys.memory.used == 30801195008
        assert sys.memory.free == 812224126976
        assert sys.memory.avail == 977440014336

    @patch('igm.env.system.get_memory_info', MagicMock(return_value=MEMORY_INFO_100))
    def test_swap(self):
        assert not sys.swap
        assert sys.swap.total == 0
        assert sys.swap.used == 0
        assert sys.swap.free == 0
        assert sys.swap.avail is None

    def test_memory_actual(self):
        assert sys.memory
        assert sys.memory.total == psutil.virtual_memory().total

    @skipUnless(psutil.swap_memory().total, 'swap memory required')
    def test_swap_actual(self):
        assert sys.swap
        assert sys.swap.total == psutil.swap_memory().total

    @skipUnless(not psutil.swap_memory().total, 'no swap memory required')
    def test_no_swap_actual(self):
        assert not sys.swap

    @pytest.mark.flaky(reruns=3, reruns_delay=CONNECT_CACHE_TTL)
    @skipUnless(not os.getenv('NO_INTERNET'), 'sys.internet required')
    @skipUnless(not os.getenv('NO_GFW'), 'gfw required')
    @skipUnless(not os.getenv('NO_ACTUAL'), 'actual is skipped')
    def test_internet_actual_has_internet_in_gfw(self):
        assert sys.internet
        assert sys.internet.has_internet
        assert sys.internet.has_gfw
        assert repr(sys.internet) == '<Internet ok, gfw: yes>'

        assert sys.internet.baidu
        assert sys.internet.gitee
        assert sys.internet.github
        assert not sys.internet.google

        assert sys.internet.baidu
        assert sys.internet.baidu.ok
        assert 0.0 <= sys.internet.baidu.ttl <= 1.0
        assert sys.internet.baidu.address == 'baidu.com'
        assert sys.internet.baidu.port == 80
        assert repr(sys.internet.baidu).startswith('<BaiduConnect baidu.com:80, success, ttl:') and \
               repr(sys.internet.baidu).endswith('ms>')

        assert not sys.internet.google
        assert not sys.internet.google.ok
        assert sys.internet.google.ttl is None
        assert sys.internet.google.address == 'google.com'
        assert sys.internet.google.port == 80
        assert repr(sys.internet.google) == '<GoogleConnect google.com:80, fail>'

        assert not sys.internet('twitter.com')
        assert not sys.internet('twitter.com')
        assert sys.internet('twitter.com').ttl is None
        assert sys.internet('twitter.com').address == 'twitter.com'
        assert sys.internet('twitter.com').port == 80
        assert repr(sys.internet('twitter.com')) == '<ConnectStatus twitter.com:80, fail>'

    @pytest.mark.flaky(reruns=3, reruns_delay=CONNECT_CACHE_TTL)
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    @skipUnless(os.getenv('NO_GFW'), 'no gfw required')
    @skipUnless(not os.getenv('NO_ACTUAL'), 'actual is skipped')
    def test_internet_actual_has_internet_out_of_gfw(self):
        assert sys.internet
        assert sys.internet.has_internet
        assert not sys.internet.has_gfw
        assert repr(sys.internet) == '<Internet ok, gfw: no>'

        assert sys.internet.baidu
        assert sys.internet.gitee
        assert sys.internet.github
        assert sys.internet.google

        assert sys.internet.baidu
        assert sys.internet.baidu.ok
        assert 0.0 <= sys.internet.baidu.ttl <= 1.0
        assert sys.internet.baidu.address == 'baidu.com'
        assert sys.internet.baidu.port == 80
        assert repr(sys.internet.baidu).startswith('<BaiduConnect baidu.com:80, success, ttl:') and \
               repr(sys.internet.baidu).endswith('ms>')

        assert sys.internet.google
        assert sys.internet.google.ok
        assert 0.0 <= sys.internet.google.ttl <= 1.0
        assert sys.internet.google.address == 'google.com'
        assert sys.internet.google.port == 80
        assert repr(sys.internet.google).startswith('<GoogleConnect google.com:80, success, ttl:') and \
               repr(sys.internet.google).endswith('ms>')

    @skipUnless(os.getenv('NO_INTERNET'), 'no internet required')
    @skipUnless(not os.getenv('NO_ACTUAL'), 'actual is skipped')
    def test_internet_actual_no_network(self):
        assert not sys.internet
        assert not sys.internet.has_internet
        assert repr(sys.internet) == '<Internet unavailable>'

    @skipUnless(is_windows(), 'windows only')
    def test_os_actual_on_windows(self):
        assert sys.os.type == 'win'

    @skipUnless(is_linux(), 'linux only')
    def test_os_actual_on_linux(self):
        assert sys.os.type == 'linux'

    @skipUnless(is_macos(), 'macos only')
    def test_os_actual_on_macos(self):
        assert sys.os.type == 'mac'

    def test_python_info_actual(self):
        assert sys.python.version == platform.python_version()
        assert sys.python.implement == platform.python_implementation()

    def test_pip_actual(self):
        assert sys.pip.version == package_version('pip')
        assert sys.pip('hbutils').name == 'hbutils'
        assert sys.pip('hbutils').version == package_version('hbutils')

        assert str(sys.pip) == f'<Pip version: {package_version("pip")}>'
        assert repr(sys.pip) == f'<Pip version: {package_version("pip")}>'

        assert str(sys.pip('hbutils')) == f'hbutils=={package_version("hbutils")}'
        assert repr(sys.pip('hbutils')) == f'<PipPackage hbutils, version: {package_version("hbutils")}>'

    def test_sys_repr(self):
        assert str(sys).startswith('<SystemInfo')
        assert repr(sys).startswith('<SystemInfo')
