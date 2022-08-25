import os

import pytest

from igm.env.hardware.cpu import CPUArch, CPUSet, get_cpu_info


@pytest.mark.unittest
class TestEnvHardwareCpu:
    def test_cpuarch(self):
        assert CPUArch.ARM_7 == CPUArch.ARM_7
        assert CPUArch.ARM_7 != CPUArch.ARM_8
        assert CPUArch.ARM_7 == 'arm_7'
        assert CPUArch.ARM_7 == 'Arm_7'
        assert CPUArch.ARM_7 != None
        assert CPUArch.ARM_7 != 30

        assert str(CPUArch.ARM_7) == 'arm_7'
        assert repr(CPUArch.ARM_7) == '<CPUArch arm_7>'

    def test_cpuset_info(self, cpu_1, cpu_2, cpu_100):
        assert cpu_1
        assert cpu_1.num == 6
        assert cpu_1.brand == 'Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz'
        assert cpu_1.arch == 'x86_64'

        assert cpu_2
        assert cpu_2.num == 12
        assert cpu_2.brand == 'Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz'
        assert cpu_2.arch == 'x86_64'

        assert cpu_100
        assert cpu_100.num == 112
        assert cpu_100.brand == 'Intel(R) Xeon(R) Gold 6348 CPU @ 2.60GHz'
        assert cpu_100.arch == 'X86_64'

    def test_cpuset_usage(self, cpu_1, cpu_2, cpu_100):
        assert cpu_1.usage.ratio == pytest.approx(0.20016666666666666)
        assert cpu_2.usage.ratio == pytest.approx(0.17175)
        assert cpu_100.usage.ratio == pytest.approx(0.015669642857142858)

    def test_cpuset_frequency(self, cpu_1, cpu_2, cpu_100):
        assert cpu_1.frequency == pytest.approx(2592.002)
        assert cpu_2.frequency == pytest.approx(2592.0)
        assert cpu_100.frequency == pytest.approx(3399.988473214286)

    def test_cpuset_str(self, cpu_1, cpu_2, cpu_100):
        assert str(cpu_1) == '<CPUSet Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz, ' \
                             'arch: x86_64, 6 cpus, usage: 20.02%, freq: 2592.00 MHz>'
        assert str(cpu_2) == '<CPUSet Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz, ' \
                             'arch: x86_64, 12 cpus, usage: 17.18%, freq: 2592.00 MHz>'
        assert str(cpu_100) == '<CPUSet Intel(R) Xeon(R) Gold 6348 CPU @ 2.60GHz, ' \
                               'arch: x86_64, 112 cpus, usage: 1.57%, freq: 3399.99 MHz>'

    def test_cpuset_repr(self, cpu_1, cpu_2, cpu_100):
        assert repr(cpu_1) == '<CPUSet Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz, ' \
                              'arch: x86_64, 6 cpus, usage: 20.02%, freq: 2592.00 MHz>'
        assert repr(cpu_2) == '<CPUSet Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz, ' \
                              'arch: x86_64, 12 cpus, usage: 17.18%, freq: 2592.00 MHz>'
        assert repr(cpu_100) == '<CPUSet Intel(R) Xeon(R) Gold 6348 CPU @ 2.60GHz, ' \
                                'arch: x86_64, 112 cpus, usage: 1.57%, freq: 3399.99 MHz>'

    def test_cpu_id(self, cpu_1, cpu_2, cpu_100):
        for i in range(cpu_1.num):
            assert cpu_1[i].id == i

        for i in range(cpu_2.num):
            assert cpu_2[i].id == i

        for i in range(cpu_100.num):
            assert cpu_100[i].id == i

    def test_cpu_percentage(self, cpu_1):
        assert cpu_1[0].usage.ratio == pytest.approx(0.082)
        assert cpu_1[1].usage.ratio == pytest.approx(0.055)
        assert cpu_1[2].usage.ratio == pytest.approx(0.018)
        assert cpu_1[3].usage.ratio == pytest.approx(0.037)
        assert cpu_1[4].usage.ratio == pytest.approx(0.036)
        assert cpu_1[5].usage.ratio == pytest.approx(0.973)

    def test_cpu_frequency(self, cpu_1):
        assert cpu_1[0].frequency == pytest.approx(2592.002)
        assert cpu_1[1].frequency == pytest.approx(2592.002)
        assert cpu_1[2].frequency == pytest.approx(2592.002)
        assert cpu_1[3].frequency == pytest.approx(2592.002)
        assert cpu_1[4].frequency == pytest.approx(2592.002)
        assert cpu_1[5].frequency == pytest.approx(2592.002)

    def test_cpu_repr(self, cpu_1):
        assert repr(cpu_1[0]) == '<CPU #0, usage: 8.20%, freq: 2592.00 MHz>'
        assert repr(cpu_1[1]) == '<CPU #1, usage: 5.50%, freq: 2592.00 MHz>'
        assert repr(cpu_1[2]) == '<CPU #2, usage: 1.80%, freq: 2592.00 MHz>'
        assert repr(cpu_1[3]) == '<CPU #3, usage: 3.70%, freq: 2592.00 MHz>'
        assert repr(cpu_1[4]) == '<CPU #4, usage: 3.60%, freq: 2592.00 MHz>'
        assert repr(cpu_1[5]) == '<CPU #5, usage: 97.30%, freq: 2592.00 MHz>'

    def test_actual_run(self):
        cpuset = CPUSet(get_cpu_info())
        assert cpuset.num == os.cpu_count()
        assert cpuset.brand
        assert cpuset.arch
