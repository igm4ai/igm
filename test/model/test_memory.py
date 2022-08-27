import pytest

from igm.model import MemoryStatus


@pytest.fixture()
def mem_724():
    return MemoryStatus('7GiB', '2.4GB')


class ExampleMemoryStatus(MemoryStatus):
    def __init__(self, data):
        MemoryStatus.__init__(self, data['total'], data['used'], data['free'])


@pytest.fixture()
def mem_actual():
    return ExampleMemoryStatus({
        "total": "12021 MiB",
        "used": "140 MiB",
        "free": "11881 MiB"
    })


@pytest.fixture()
def mem_0():
    return MemoryStatus(0, 0, 0, 0)


@pytest.fixture()
def mem_avail():
    return MemoryStatus('7GiB', '2.4GB', '3.2GB', '5GiB')


@pytest.mark.unittest
class TestModelMemory:
    def test_common(self, mem_724, mem_actual, mem_avail, mem_0):
        assert mem_724.total.bytes == 7516192768
        assert mem_724.free.bytes == 5116192768
        assert mem_724.used.bytes == 2400000000
        assert mem_724.avail is None

        assert mem_actual.total.bytes == 12604932096
        assert mem_actual.free.bytes == 12458131456
        assert mem_actual.used.bytes == 146800640
        assert mem_actual.avail is None

        assert mem_avail.total.bytes == 7516192768
        assert mem_avail.free.bytes == 3200000000
        assert mem_avail.used.bytes == 2400000000
        assert mem_avail.avail.bytes == 5368709120

        assert mem_0.total.bytes == 0
        assert mem_0.free.bytes == 0
        assert mem_0.used.bytes == 0
        assert mem_0.avail.bytes == 0

    def test_percentage(self, mem_724, mem_actual, mem_avail, mem_0):
        assert mem_724.free_percentage.percentage == pytest.approx(68.06894029889789)
        assert mem_724.used_percentage.percentage == pytest.approx(31.93105970110212)
        assert mem_724.avail_percentage is None

        assert mem_actual.free_percentage.percentage == pytest.approx(98.83537143332501)
        assert mem_actual.used_percentage.percentage == pytest.approx(1.1646285666749854)
        assert mem_actual.avail_percentage is None

        assert mem_avail.free_percentage.percentage == pytest.approx(42.57474626813616)
        assert mem_avail.used_percentage.percentage == pytest.approx(31.93105970110212)
        assert mem_avail.avail_percentage.percentage == pytest.approx(71.42857142857143)

        assert mem_0.free_percentage is None
        assert mem_0.used_percentage is None
        assert mem_0.avail_percentage is None

    def test_repr(self, mem_724, mem_actual, mem_0, mem_avail):
        assert repr(mem_724) == '<MemoryStatus total: 7.00 GiB, used: 2.24 GiB (31.93%), free: 4.76 GiB (68.07%)>'
        assert repr(mem_actual) == '<ExampleMemoryStatus total: 11.74 GiB, ' \
                                   'used: 140.00 MiB (1.16%), free: 11.60 GiB (98.84%)>'
        assert repr(mem_0) == '<MemoryStatus total: 0.00 Bit>'
        assert repr(mem_avail) == '<MemoryStatus total: 7.00 GiB, used: 2.24 GiB (31.93%), ' \
                                  'free: 2.98 GiB (42.57%), avail: 5.00 GiB (71.43%)>'

    def test_bool(self, mem_724, mem_actual, mem_0, mem_avail):
        assert mem_724
        assert mem_actual
        assert not mem_0
        assert mem_avail
