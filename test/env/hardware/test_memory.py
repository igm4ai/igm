import psutil
import pytest

from igm.env.hardware import get_memory_info, VirtualMemory, SwapMemory


@pytest.mark.unittest
class TestEnvHardwareMemory:
    def test_mem_info(self, mem_1, mem_2, mem_100):
        assert mem_1.total == 12550504448
        assert mem_1.free == 351268864
        assert mem_1.used == 9921683456
        assert mem_1.avail == 2254102528
        assert mem_1.used_percentage.ratio == pytest.approx(0.790540611105164)
        assert mem_1.free_percentage.ratio == pytest.approx(0.027988425919882196)
        assert mem_1.avail_percentage.ratio == pytest.approx(0.1796025440522596)

    def test_mem_repr(self, mem_1, mem_2, mem_100):
        assert repr(mem_1) == '<VirtualMemory total: 11.689 GiB, used: 9.240 GiB (79.05%), ' \
                              'free: 334.996 MiB (2.80%), avail: 2.099 GiB (17.96%)>'
        assert repr(mem_2) == '<VirtualMemory total: 63.757 GiB, used: 28.563 GiB (44.80%), ' \
                              'free: 35.194 GiB (55.20%), avail: 35.194 GiB (55.20%)>'
        assert repr(mem_100) == '<VirtualMemory total: 944.353 GiB, used: 28.686 GiB (3.04%), ' \
                                'free: 756.443 GiB (80.10%), avail: 910.312 GiB (96.40%)>'

    def test_mem_bool(self, mem_1, mem_2, mem_100):
        assert mem_1
        assert mem_2
        assert mem_100

    def test_swap_info(self, swap_1, swap_2, swap_100):
        assert swap_1.total == 2147479552
        assert swap_1.used == 2147479552
        assert swap_1.free == 0
        assert swap_1.avail is None
        assert swap_1.used_percentage.ratio == pytest.approx(1.0)
        assert swap_1.free_percentage.ratio == pytest.approx(0.0)
        assert swap_1.avail_percentage is None

        assert swap_100.total == 0
        assert swap_100.used == 0
        assert swap_100.free == 0
        assert swap_100.avail is None
        assert swap_100.used_percentage is None
        assert swap_100.free_percentage is None
        assert swap_100.avail_percentage is None

    def test_swap_bool(self, swap_1, swap_2, swap_100):
        assert swap_1
        assert swap_2
        assert not swap_100

    def test_mem_actual(self):
        mem = VirtualMemory(get_memory_info())
        assert mem.total == psutil.virtual_memory().total

    def test_swap_actual(self):
        swap = SwapMemory(get_memory_info())
        assert swap.total == psutil.swap_memory().total
