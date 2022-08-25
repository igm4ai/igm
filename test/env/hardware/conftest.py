import pytest

from igm.env.hardware import CUDA, CPUSet, VirtualMemory, SwapMemory
from ...testings import ONE_GPU_1_DATA, ONE_GPU_2_DATA, TWO_GPU_DATA, CPU_INFO_1, CPU_INFO_100, CPU_INFO_2, \
    MEMORY_INFO_1, MEMORY_INFO_2, MEMORY_INFO_100


@pytest.fixture()
def cuda_1gpu_1():
    return CUDA(ONE_GPU_1_DATA)


@pytest.fixture()
def cuda_1gpu_2():
    return CUDA(ONE_GPU_2_DATA)


@pytest.fixture()
def cuda_2gpus():
    return CUDA(TWO_GPU_DATA)


@pytest.fixture()
def cpu_1():
    return CPUSet(CPU_INFO_1)


@pytest.fixture()
def cpu_2():
    return CPUSet(CPU_INFO_2)


@pytest.fixture()
def cpu_100():
    return CPUSet(CPU_INFO_100)


@pytest.fixture()
def mem_1():
    return VirtualMemory(MEMORY_INFO_1)


@pytest.fixture()
def mem_2():
    return VirtualMemory(MEMORY_INFO_2)


@pytest.fixture()
def mem_100():
    return VirtualMemory(MEMORY_INFO_100)


@pytest.fixture()
def swap_1():
    return SwapMemory(MEMORY_INFO_1)


@pytest.fixture()
def swap_2():
    return SwapMemory(MEMORY_INFO_2)


@pytest.fixture()
def swap_100():
    return SwapMemory(MEMORY_INFO_100)
