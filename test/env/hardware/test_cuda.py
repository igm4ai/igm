import pytest

from igm.env.hardware import CUDA


@pytest.mark.unittest
class TestEnvHardwareCuda:
    def test_type(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert isinstance(cuda_1gpu_1, CUDA)
        assert isinstance(cuda_1gpu_2, CUDA)
        assert isinstance(cuda_2gpus, CUDA)

    def test_version(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert cuda_1gpu_1.version == '11.4'
        assert cuda_1gpu_2.version == '11.6'
        assert cuda_2gpus.version == '11.2'

    def test_driver_version(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert cuda_1gpu_1.driver_version == '470.141.3'
        assert cuda_1gpu_2.driver_version == '512.92'
        assert cuda_2gpus.driver_version == '460.32.3'

    def test_gpus_count(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert cuda_1gpu_1.gpus.num == 1
        assert cuda_1gpu_2.gpus.num == 1
        assert cuda_2gpus.gpus.num == 2

    def test_str(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert str(cuda_1gpu_1) == '<CUDA 11.4, driver: 470.141.3>'
        assert str(cuda_1gpu_2) == '<CUDA 11.6, driver: 512.92>'
        assert str(cuda_2gpus) == '<CUDA 11.2, driver: 460.32.3>'

    def test_repr(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert repr(cuda_1gpu_1) == '<CUDA 11.4, driver: 470.141.3>'
        assert repr(cuda_1gpu_2) == '<CUDA 11.6, driver: 512.92>'
        assert repr(cuda_2gpus) == '<CUDA 11.2, driver: 460.32.3>'

    def test_keys(self, cuda_1gpu_1, cuda_1gpu_2, cuda_2gpus):
        assert list(cuda_1gpu_1.keys()) == ['timestamp', 'driver_version', 'cuda_version', 'attached_gpus', 'gpu']
        assert list(cuda_1gpu_2.keys()) == ['timestamp', 'driver_version', 'cuda_version', 'attached_gpus', 'gpu']
        assert list(cuda_2gpus.keys()) == ['timestamp', 'driver_version', 'cuda_version', 'attached_gpus', 'gpu']
