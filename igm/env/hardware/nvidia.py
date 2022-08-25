import os
import subprocess
import time
import warnings
from functools import lru_cache

import xmltodict
from hbutils.system import which

from .base import RESOURCE_TIMEOUT


class NvidiaSmiNotFound(Exception):
    pass


class NvidiaSmiFailed(Exception):
    pass


NVIDIA_SMI_CMD = which('nvidia-smi')


@lru_cache()
def _nvidia_smi_info(ttl_hash):
    _ = ttl_hash
    if not NVIDIA_SMI_CMD:
        raise NvidiaSmiNotFound('nvidia-smi not found in current environment.')

    process = subprocess.Popen([NVIDIA_SMI_CMD, '-x', '-q'], stdout=subprocess.PIPE)
    (stdout, stderr) = process.communicate()
    exit_code = process.wait()

    if exit_code:
        raise NvidiaSmiFailed(exit_code, stderr)
    if stderr and stderr.strip():
        warnings.warn(f'Stderr from nvidia-smi:{os.linesep}'
                      f'{stderr}')

    return xmltodict.parse(stdout)


def get_nvidia_info():
    return _nvidia_smi_info(int(time.time() // RESOURCE_TIMEOUT))
