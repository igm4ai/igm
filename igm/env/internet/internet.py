import time
from functools import lru_cache
from typing import Type, TypeVar

from .connect import CONNECT_TIMEOUT
from .connect import try_connect as _origin_try_connect

DEFAULT_PORT = 80
GLOBAL_DNS_HOST = ('8.8.4.4', 53)

GOOGLE_HOST = ('google.com', 80)
GITHUB_HOST = ('github.com', 80)

BAIDU_HOST = ('baidu.com', 80)
GITEE_HOST = ('gitee.com', 80)

PING_MIN_TIMEOUT = 5


@lru_cache()
def _try_connect_once(address: str, port: int, timeout: int, ttl_hash: int):
    _ = ttl_hash
    return _origin_try_connect(address, port, timeout)


class ConnectStatus:
    def __init__(self, address: str, port: int, ok: bool, ttl: float):
        self.__address = address
        self.__port = port
        self.__ok = ok
        self.__ttl = ttl

    @property
    def ok(self) -> bool:
        return self.__ok

    @property
    def ttl(self) -> float:
        return self.__ttl

    @property
    def address(self) -> str:
        return self.__address

    @property
    def port(self) -> int:
        return self.__port

    def __bool__(self):
        return bool(self.__ok)

    def __repr__(self):
        if self.ok:
            return f'<{type(self).__name__} {self.address}:{self.port}, success, ttl: {self.ttl * 1000.0:.2f}ms>'
        else:
            return f'<{type(self).__name__} {self.address}:{self.port}, fail>'


_ConnectStatusType = TypeVar('_ConnectStatusType', bound=ConnectStatus)


def _try_connect(address: str, port: int, timeout: int = CONNECT_TIMEOUT,
                 clazz: Type[_ConnectStatusType] = ConnectStatus) -> _ConnectStatusType:
    ok, ttl = _try_connect_once(address, port, timeout, int(time.time() // PING_MIN_TIMEOUT))
    return clazz(address, port, ok, ttl)


class GlobalDNSConnect(ConnectStatus):
    pass


class GoogleConnect(ConnectStatus):
    pass


class GithubConnect(ConnectStatus):
    pass


class BaiduConnect(ConnectStatus):
    pass


class GiteeConnect(ConnectStatus):
    pass


class Internet:
    def __call__(self, address: str, port: int = 80, *, timeout: int = CONNECT_TIMEOUT):
        return _try_connect(address, port, timeout=timeout)

    @property
    def dns(self) -> GlobalDNSConnect:
        return _try_connect(*GLOBAL_DNS_HOST, clazz=GlobalDNSConnect)

    @property
    def google(self) -> GoogleConnect:
        return _try_connect(*GOOGLE_HOST, clazz=GoogleConnect)

    @property
    def github(self) -> GithubConnect:
        return _try_connect(*GITHUB_HOST, clazz=GithubConnect)

    @property
    def baidu(self) -> BaiduConnect:
        return _try_connect(*BAIDU_HOST, clazz=BaiduConnect)

    @property
    def gitee(self) -> GiteeConnect:
        return _try_connect(*GITEE_HOST, clazz=GiteeConnect)

    def __bool__(self) -> bool:
        return self.has_internet

    @property
    def has_internet(self) -> bool:
        return bool(self.dns)

    @property
    def has_gfw(self) -> bool:
        return not bool(self.google)

    def __repr__(self):
        if self.has_internet:
            return f'<{type(self).__name__} ok, gfw: {"yes" if self.has_gfw else "no"}>'
        else:
            return f'<{type(self).__name__} unavailable>'


internet = Internet()
