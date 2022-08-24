import time
from functools import lru_cache

import psutil

from .base import RESOURCE_TIMEOUT
from ...model import MemoryStatus


@lru_cache()
def _get_memory_info(ttl_hash):
    _ = ttl_hash
    return psutil.virtual_memory(), psutil.swap_memory()


def get_memory_info():
    return _get_memory_info(int(time.time() // RESOURCE_TIMEOUT))


class VirtualMemory(MemoryStatus):
    def __init__(self, data):
        virtual, _ = data
        MemoryStatus.__init__(self, virtual.total, virtual.used, virtual.free, virtual.available)


class SwapMemory(MemoryStatus):
    def __init__(self, data):
        _, swap = data
        MemoryStatus.__init__(self, swap.total, swap.used, swap.free)
