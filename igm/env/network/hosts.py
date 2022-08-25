from typing import Tuple, List

from hbutils.system import is_windows


def _get_host_filename():
    if is_windows():
        return r"c:\windows\system32\drivers\etc\hosts"
    else:
        return '/etc/hosts'


def get_hosts() -> List[Tuple[str, str]]:
    host_list = []
    with open(_get_host_filename(), 'r') as hf:
        for line in hf:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            _content, *_ = line.split('#', maxsplit=1)
            ip_address, *hostnames = _content.strip().split()
            for host in hostnames:
                host_list.append((host.strip(), ip_address.strip()))

    return host_list


_LOCALHOST = 'localhost'
_DEFAULT_LOCALHOST = '127.0.0.1'


def get_localhost() -> str:
    for hostname, ip_address in get_hosts():
        if hostname == _LOCALHOST:
            return ip_address

    return _DEFAULT_LOCALHOST
