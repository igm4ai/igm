import socket
from unittest.mock import patch, MagicMock

import pytest


class _TestSocketError(socket.error):
    pass


@pytest.fixture()
def no_connect_cache():
    with patch('igm.env.internet.net.CONNECT_CACHE_TTL', None):
        yield


@pytest.fixture()
def no_network(no_connect_cache):
    def _connect(address):
        raise _TestSocketError('The network cable has been unplugged')

    with patch('socket.socket.connect', MagicMock(side_effect=_connect)):
        yield


_WALLED_WORDS = ['google', 'twitter']


@pytest.fixture()
def network_in_gfw(no_connect_cache):
    def _connect(address):
        host, port = address
        if any(map(lambda x: x in host, _WALLED_WORDS)):
            raise _TestSocketError(f'The site is blocked because of gfw :)')
        else:
            return None

    with patch('socket.socket.connect', MagicMock(side_effect=_connect)):
        yield


@pytest.fixture()
def network_out_of_gfw(no_connect_cache):
    def _connect(address):
        return None

    with patch('socket.socket.connect', MagicMock(side_effect=_connect)):
        yield
