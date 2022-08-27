import contextlib
import inspect
import os
from typing import Dict, ContextManager, List, Union

from hbutils.random import random_sha1_with_timestamp

from .requirement import load_req
from .template import IGMTemplate
from ..utils import get_global, with_pythonpath, retrieve

_IGM_SESSIONS: Dict[str, IGMTemplate] = {}
_IGM_SESSION_ID_NAME = '__igm_session_id__'
_IGM_PATH_NAME = '__igm_path__'

_DEFAULT_REQUIREMENTS_TXT = 'requirements.txt'


def igm_setup(
        *,
        name: str,
        version: str,
        description: str,
        template_dir='template',
        requirements: Union[List[str], str, None] = None,
) -> IGMTemplate:
    outer_frame = inspect.currentframe().f_back
    outer_dir, _ = os.path.split(os.path.abspath(outer_frame.f_code.co_filename))

    session_id = get_global(_IGM_SESSION_ID_NAME, default=None)
    path = get_global(_IGM_PATH_NAME, default=outer_dir)

    if isinstance(requirements, str) or \
            (requirements is None and os.path.exists(os.path.join(path, _DEFAULT_REQUIREMENTS_TXT))):
        reqfile = requirements if isinstance(requirements, str) \
            else os.path.join(path, _DEFAULT_REQUIREMENTS_TXT)
        requirements = load_req(reqfile)
    elif requirements is None:
        requirements = []
    elif isinstance(requirements, (list, tuple)):
        requirements = list(filter(lambda x: x.strip(), requirements))
    else:
        raise TypeError(f'Unknown requirements - {requirements!r}.')

    retval = IGMTemplate(
        # meta information
        name, version, description,

        # directory configuration
        path=path,
        template_dir=template_dir,

        # dependency
        requirements=requirements,
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
