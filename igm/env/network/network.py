import time
from functools import lru_cache
from typing import Type, TypeVar

from .hosts import get_localhost
from .ping import DEFAULT_TIMEOUT, ping

GLOBAL_DNS_HOST = '8.8.8.8'

GOOGLE_HOST = 'google.com'
GITHUB_HOST = 'github.com'

BAIDU_HOST = 'baidu.com'
GITEE_HOST = 'gitee.com'

PING_MIN_TIMEOUT = 5


@lru_cache()
def _ping_once(address, timeout: int, ttl_hash: int):
    _ = ttl_hash

    return ping(address, timeout)


class PingStatus:
    def __init__(self, address: str, ok: bool, ttl: float):
        self.__address = address
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

    def __bool__(self):
        return bool(self.__ok)

    def __repr__(self):
        if self.ok:
            return f'<{type(self).__name__} {self.address}, success, ttl: {self.ttl * 1000.0:.2f}ms>'
        else:
            return f'<{type(self).__name__} {self.address}, fail>'


_PingStatusType = TypeVar('_PingStatusType', bound=PingStatus)


def _ping(address, timeout: int = DEFAULT_TIMEOUT, clazz: Type[_PingStatusType] = PingStatus) -> _PingStatusType:
    ok, ttl = _ping_once(address, timeout, int(time.time() // PING_MIN_TIMEOUT))
    return clazz(address, ok, ttl)


class LocalhostPing(PingStatus):
    pass


class DNSPing(PingStatus):
    pass


class GooglePing(PingStatus):
    pass


class GithubPing(PingStatus):
    pass


class BaiduPing(PingStatus):
    pass


class GiteePing(PingStatus):
    pass


class Network:
    def __call__(self, address: str, *, timeout: int = DEFAULT_TIMEOUT):
        return _ping(address, timeout=timeout)

    @property
    def dns(self) -> DNSPing:
        return _ping(GLOBAL_DNS_HOST, clazz=DNSPing)

    @property
    def localhost(self) -> LocalhostPing:
        return _ping(get_localhost(), clazz=LocalhostPing)

    @property
    def google(self) -> GooglePing:
        return _ping(GOOGLE_HOST, clazz=GooglePing)

    @property
    def github(self) -> GithubPing:
        return _ping(GITHUB_HOST, clazz=GithubPing)

    @property
    def baidu(self) -> BaiduPing:
        return _ping(BAIDU_HOST, clazz=BaiduPing)

    @property
    def gitee(self) -> GiteePing:
        return _ping(GITEE_HOST, clazz=GiteePing)

    def __bool__(self) -> bool:
        return bool(self.localhost)

    @property
    def has_internet(self) -> bool:
        return bool(self.dns)

    @property
    def has_gfw(self) -> bool:
        return not bool(self.google)

    def __repr__(self):
        if self:
            if self.has_internet:
                return f'<{type(self).__name__} ok, internet: ok, ' \
                       f'gfw: {"yes" if self.has_gfw else "no"}>'
            else:
                return f'<{type(self).__name__} ok, internet: unavailable>'
        else:
            return f'<{type(self).__name__} unavailable>'


network = Network()
