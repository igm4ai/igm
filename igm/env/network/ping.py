from typing import Tuple, Optional

import ping3
from ping3.errors import PingError

DEFAULT_TIMEOUT = 1


def ping(address, timeout=DEFAULT_TIMEOUT) -> Tuple[bool, Optional[float]]:
    try:
        retval = ping3.ping(address, timeout=timeout, unit='s')
    except PingError:
        return False, None
    else:
        if retval is None or (isinstance(retval, bool) and not retval):
            return False, None
        else:
            return True, retval
