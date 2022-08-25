from shutil import which
from unittest import skipUnless
from unittest.mock import patch

import pytest

from igm.env.hardware import get_nvidia_info
from igm.env.hardware.nvidia import NvidiaSmiNotFound


@pytest.mark.unittest
class TestEnvHardwareNvidia:
    @patch('igm.env.hardware.nvidia.NVIDIA_SMI_CMD', None)
    def test_get_nvidia_info_not_found(self):
        with pytest.raises(NvidiaSmiNotFound):
            _ = get_nvidia_info()

    @skipUnless(which('nvidia-smi'), 'nvidia-smi cli required')
    def test_get_nvidia_info_actual(self):
        data = get_nvidia_info()
        assert isinstance(data, dict)
        assert "nvidia_smi_log" in data

        log = data["nvidia_smi_log"]
        assert "timestamp" in log
        assert "cuda_version" in log
        assert "driver_version" in log
        assert "attached_gpus" in log
        assert "gpu" in log
        assert isinstance(log['gpu'], (dict, list))
