from typing import Optional

from .hardware import get_cpu_info, CPUCollection, CUDA, GPUCollection, get_memory_info, SwapMemory, VirtualMemory, \
    get_nvidia_info
from .hardware.nvidia import NvidiaSmiNotFound


class SystemInfo:
    @property
    def cpu(self) -> CPUCollection:
        return CPUCollection(get_cpu_info())

    @property
    def memory(self) -> VirtualMemory:
        return VirtualMemory(get_memory_info())

    @property
    def swap(self) -> SwapMemory:
        return SwapMemory(get_memory_info())

    @property
    def cuda(self) -> Optional[CUDA]:
        try:
            return CUDA(get_nvidia_info())
        except NvidiaSmiNotFound:
            return None

    @property
    def gpu(self) -> Optional[GPUCollection]:
        cuda = self.cuda
        if cuda:
            return cuda.gpus
        else:
            return None


sys = SystemInfo()
