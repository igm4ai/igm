import os.path
import shlex
import subprocess
import sys
from typing import Union, List, Any, Mapping, Optional

from hbutils.reflection import mount_pythonpath
from hbutils.string import plural_word

from ..utils import get_globals


class IGMScript:
    def describe(self) -> str:
        raise NotImplementedError  # pragma: no cover

    def run(self):
        raise NotImplementedError  # pragma: no cover


class IGMFuncScript(IGMScript):
    def __init__(self, func):
        self.func = func

    def describe(self) -> str:
        if hasattr(self.func, '__doc__') and self.func.__doc__.strip():
            return self.func.__doc__.strip()
        else:
            return f'Call function {self.func.__name__!r}.'

    def run(self):
        self.func()


def _trans_command(command: Union[List[str], str]) -> List[str]:
    if isinstance(command, str):
        return shlex.split(command)
    else:
        return command


def _repr_command(command: Union[List[str], str]) -> str:
    return ' '.join(map(shlex.quote, _trans_command(command)))


class IGMCommandScript(IGMScript):
    def __init__(self, command: Union[List[str], str]):
        self.command = _trans_command(command)

    def _visual_command(self) -> List[str]:
        return self.command

    def describe(self) -> str:
        return f'Command - {_repr_command(self._visual_command())}'

    def run(self):
        print(_repr_command(self.command))
        process = subprocess.run(self.command)
        try:
            process.check_returncode()
        finally:
            print()


class IGMPythonScript(IGMCommandScript):
    def __init__(self, command: Union[List[str], str]):
        self._python_command = _trans_command(command)
        IGMCommandScript.__init__(self, [sys.executable, *self._python_command])

    def _visual_command(self) -> List[str]:
        return ['python', *self._python_command]


class IGMPipScript(IGMPythonScript):
    def __init__(self, command: Union[List[str], str]):
        self._pip_command = _trans_command(command)
        IGMPythonScript.__init__(self, ['-m', 'pip', *self._pip_command])

    def _visual_command(self) -> List[str]:
        return ['pip', *self._pip_command]


class IGMScriptSet(IGMScript):
    def __init__(self, *scripts, desc: Optional[str] = None):
        self.scripts = scripts
        self.desc = desc

    def describe(self) -> str:
        return self.desc or f'Run a set of {plural_word(len(self.scripts), "scripts")} in order.'

    def run(self):
        for script in self.scripts:
            script()


def _to_script(v):
    if isinstance(v, IGMScript):
        return v
    elif isinstance(v, str):
        return IGMCommandScript(v)
    elif callable(v):
        return IGMFuncScript(v)
    elif isinstance(v, (list, tuple)):
        if all([isinstance(x, str) for x in v]):
            return IGMCommandScript(v)
        else:
            return IGMScriptSet(*map(_to_script, v))
    else:
        raise TypeError(f'Unknown script type - {v!r}.')


def cpy(command: Union[List[str], str]) -> IGMPythonScript:
    return IGMPythonScript(command)


def cpip(command: Union[List[str], str]) -> IGMPipScript:
    return IGMPipScript(command)


def cmds(description: str, v: List) -> IGMScriptSet:
    return IGMScriptSet(*map(_to_script, v), desc=description)


class IGMProject:
    def __init__(self, name, version, template_name, template_version, created_at, params, scripts):
        self.name = name
        self.version = version
        self.template_name = template_name
        self.template_version = template_version
        self.created_at = created_at
        self.params = dict(params or {})
        self.scripts = dict(scripts or {})


_IGM_PROJECT_TAG = '__igm_project__'


def igm_project(
        name,
        version,
        template_name,
        template_version,
        created_at,
        params: Optional[Mapping[str, Any]] = None,
        scripts: Optional[Mapping[str, Any]] = None,
):
    g = get_globals()
    proj = IGMProject(
        name, version,
        template_name, template_version, created_at,
        params, scripts,
    )

    g[_IGM_PROJECT_TAG] = proj
    return proj


def load_igm_project(directory, meta_filename='igmeta.py') -> Optional[IGMProject]:
    if not os.path.exists(directory):
        raise FileNotFoundError(directory)

    if os.path.isfile(directory):
        proj_dir, metafile = os.path.split(os.path.abspath(directory))
    else:
        proj_dir, metafile = os.path.abspath(directory), meta_filename

    _globals = {}
    with mount_pythonpath(proj_dir):
        with open(os.path.join(proj_dir, metafile), 'r') as f:
            exec(f.read(), _globals)

    return _globals.get(_IGM_PROJECT_TAG, None)
