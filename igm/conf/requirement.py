import pathlib
import subprocess
import sys
from typing import List, Union

import pkg_resources
from hbutils.encoding import auto_decode
from pkg_resources import DistributionNotFound, VersionConflict


def load_req(filename: str) -> List[str]:
    with pathlib.Path(filename).open() as reqfile:
        return list(map(str, pkg_resources.parse_requirements(reqfile)))


def _try_autodecode(d: Union[str, bytes, bytearray, None]):
    if d is None or isinstance(d, str):
        return d
    elif isinstance(d, (bytes, bytearray)):
        return auto_decode(d)
    else:
        raise TypeError(f'Invalid type for decoding - {d!r}.')  # pragma: no cover


def pip(*args, capture_output: bool = False):
    process = subprocess.run([sys.executable, '-m', 'pip', *args], check=True, capture_output=capture_output)
    return process.returncode, _try_autodecode(process.stdout), _try_autodecode(process.stderr)


def check_req(reqs: List[str]) -> bool:
    try:
        pkg_resources.require(reqs)
    except (DistributionNotFound, VersionConflict):
        return False
    else:
        return True
