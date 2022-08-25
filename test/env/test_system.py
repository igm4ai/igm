import os
from unittest import skipUnless
from unittest.mock import patch, MagicMock

import pytest
from hbutils.system import which

from igm.env import sys
from ..testings import ONE_GPU_1_DATA, CPU_INFO_1, CPU_INFO_100


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
