import time
from functools import lru_cache

import cpuinfo
import psutil
from hbutils.string import plural_word

from .base import RESOURCE_TIMEOUT
from ...model import GenericCollection, Percentage


@lru_cache()
def _init_percent():
    _ = psutil.cpu_percent(percpu=True)


@lru_cache()
def _get_cpu_info(ttl_hash):
    _init_percent()
    _ = ttl_hash
    return {
        'count': psutil.cpu_count(),
        'brand': cpuinfo.get_cpu_info()['brand_raw'],
        'cpus': [
            {
                'percentage': perc,
                'frequency': freq.current,
            }
            for perc, freq in zip(psutil.cpu_percent(percpu=True), psutil.cpu_freq(percpu=True))
        ]
    }


def get_cpu_info():
    return _get_cpu_info(int(time.time() // RESOURCE_TIMEOUT))


def _average(ls):
    return sum(ls) / len(ls)


class CPUUsage(Percentage):
    pass


class CPUCollection(GenericCollection):
    def __init__(self, data: dict):
        GenericCollection.__init__(self, [CPU(i, item) for i, item in enumerate(data['cpus'])])
        self.__data = data

    @property
    def brand(self) -> str:
        return self.__data['brand']

    @property
    def usage(self) -> CPUUsage:
        return CPUUsage(_average([c['percentage'] / 100 for c in self.__data['cpus']]))

    @property
    def frequency(self) -> float:
        return _average([c['frequency'] for c in self.__data['cpus']])

    def __str__(self):
        return GenericCollection.__str__(self)

    def __repr__(self):
        return f'<{type(self).__name__} {plural_word(len(self), "cpu")}, ' \
               f'usage: {self.usage}, freq: {self.frequency:.2f} MHz>'


class CPU:
    def __init__(self, id_: int, data: dict):
        self.__id = id_
        self.__data = data

    @property
    def id(self):
        return self.__id

    @property
    def usage(self) -> CPUUsage:
        return CPUUsage(self.__data['percentage'] / 100)

    @property
    def frequency(self) -> float:
        return self.__data['frequency']

    def __repr__(self):
        return f'<{type(self).__name__} #{self.__id}, usage: {self.usage}, freq: {self.frequency:.2f} MHz>'
