import pytest

from igm.env.system import CUDA
from ...testings import ONE_GPU_1_DATA, ONE_GPU_2_DATA, TWO_GPU_DATA


@pytest.fixture()
def cuda_1gpu_1():
    return CUDA(ONE_GPU_1_DATA)


@pytest.fixture()
def cuda_1gpu_2():
    return CUDA(ONE_GPU_2_DATA)


@pytest.fixture()
def cuda_2gpus():
    return CUDA(TWO_GPU_DATA)
