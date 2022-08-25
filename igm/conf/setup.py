import contextlib
import inspect
import os
from typing import Dict, ContextManager

from hbutils.random import random_sha1_with_timestamp

from ..template import IGMTemplate
from ..utils import get_global, with_pythonpath, retrieve

_IGM_SESSIONS: Dict[str, IGMTemplate] = {}
_IGM_SESSION_ID_NAME = '__igm_session_id__'
_IGM_PATH_NAME = '__igm_path__'


def igm_setup(
        *,
        name: str,
        version: str,
        description: str,
        template_dir='template',
) -> IGMTemplate:
    outer_frame = inspect.currentframe().f_back
    outer_dir, _ = os.path.split(os.path.abspath(outer_frame.f_code.co_filename))

    session_id = get_global(_IGM_SESSION_ID_NAME, default=None)
    path = get_global(_IGM_PATH_NAME, default=outer_dir)

    retval = IGMTemplate(
        name, version, description,
        path, template_dir,
    )
    if session_id is not None:
        _IGM_SESSIONS[session_id] = retval
    else:
        retval.print_info()

    return retval


@contextlib.contextmanager
def load_igm_setup(template: str, *segment: str, setup_filename='meta.py') -> ContextManager[IGMTemplate]:
    with retrieve(template) as path:
        path = os.path.abspath(os.path.join(path, *segment))
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
        yield _IGM_SESSIONS[session_id]