import inspect
import os
from typing import Dict

from hbutils.random import random_sha1_with_timestamp

from ..session import IGMSession
from ..utils import get_global, with_pythonpath

_IGM_SESSIONS: Dict[str, IGMSession] = {}
_IGM_SESSION_ID_NAME = '__igm_session_id__'
_IGM_PATH_NAME = '__igm_path__'


def igm_setup(
        *,
        title: str,
        version: str,
        description: str,
        template_dir='template',
) -> IGMSession:
    outer_frame = inspect.currentframe().f_back
    outer_dir, _ = os.path.split(os.path.abspath(outer_frame.f_code.co_filename))

    session_id = get_global(_IGM_SESSION_ID_NAME, default=None)
    path = get_global(_IGM_PATH_NAME, default=outer_dir)

    retval = IGMSession(
        title, version, description,
        path, template_dir,
    )
    if session_id is not None:
        _IGM_SESSIONS[session_id] = retval
    else:
        retval.print_info()

    return retval


def load_igm_setup(path: str, setup_filename='meta.py') -> IGMSession:
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    if os.path.isfile(path):
        (pathdir, _), pathfile = os.path.split(path), path
    else:
        pathdir, pathfile = path, os.path.join(path, setup_filename)

    session_id = random_sha1_with_timestamp()

    with with_pythonpath(pathdir):
        with open(pathfile, 'r') as sf:
            exec(sf.read(), {
                _IGM_SESSION_ID_NAME: session_id,
                _IGM_PATH_NAME: pathdir,
            })

    assert session_id in _IGM_SESSIONS, f'Session {session_id!r} not found.'
    return _IGM_SESSIONS[session_id]
