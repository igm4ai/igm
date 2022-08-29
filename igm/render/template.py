import builtins
import os
import warnings
from functools import partial
from typing import List, Dict, Any, Optional, Mapping

from jinja2 import Environment
from potc import transobj as _potc_transobj
from potc.fixture.imports import ImportStatement

from .base import RenderJob, RenderTask
from .imports import PyImport


class DirectoryBasedTask(RenderTask):
    def __init__(self, srcdir: str, dststr: str, extras: Optional[Mapping[str, Any]] = None):
        self.srcdir = srcdir
        self.dstdir = dststr
        self._extras = dict(extras or {})
        RenderTask.__init__(self, self._load_jobs())

    def _load_jobs(self):
        jobs = []
        for curdir, subdirs, files in os.walk(self.srcdir):
            cur_reldir = os.path.relpath(curdir, self.srcdir)
            for file in files:
                curfile = os.path.join(cur_reldir, file)
                srcfile = os.path.join(self.srcdir, curfile)
                dstfile = os.path.join(self.dstdir, curfile)
                jobs.append(TemplateJob(srcfile, dstfile, self._extras))

        return jobs


class TemplateImportWarning(Warning):
    pass


class TemplateJob(RenderJob):
    def __init__(self, srcpath: str, dstpath: str, extras: Optional[Mapping[str, Any]] = None):
        RenderJob.__init__(self, srcpath, dstpath)
        self._imps: List[ImportStatement] = []
        self._builtins = {name: getattr(builtins, name) for name in dir(builtins) if not (name.startswith('_'))}
        self._environ = self._create_environ()
        self._extras = dict(extras or {})

    def _create_environ(self):
        environ = Environment(autoescape=False)
        for name, value in self._builtins.items():
            # register function filters
            if 'a' <= name[0] <= 'z' and name not in environ.filters:
                environ.filters[name] = value

            # register type tests
            if 'a' <= name[0] <= 'z' and isinstance(value, type) and name not in environ.tests:
                environ.tests[name] = partial(lambda y, x: isinstance(x, y), value)

        environ.filters['potc'] = self._transobj
        environ.tests['None'] = lambda x: x is None

        return environ

    def _imports(self) -> List[str]:
        return sorted(map(str, self._imps))

    def _transobj(self, x) -> str:
        result = _potc_transobj(x)
        if result.imports:
            for _import in result.imports:
                self._imps.append(_import)

        return result.code

    def _parameters(self) -> Dict[str, Any]:
        from igm.env import sys, env, user
        return {
            **self._builtins,
            **self._extras,
            'sys': sys, 'env': env, 'user': user,
            'potc': self._transobj, 'py': PyImport(),
        }

    def _run(self, log):
        log(f'Rendering from {self.srcpath!r} to {self.dstpath!r} ...')
        with open(self.srcpath, 'r') as rf:
            template = self._environ.from_string(rf.read())

        dstdir, _ = os.path.split(self.dstpath)
        if dstdir:
            os.makedirs(dstdir, exist_ok=True)
        with open(self.dstpath, 'w+') as wf:
            result = template.render(**self._parameters())
            wf.write(result)

        unimports = []
        for imp in self._imports():
            if imp not in result:
                unimports.append(imp)

        if unimports:
            warnings.warn(TemplateImportWarning(
                f'These import statement is suggested to added in template {self.srcpath!r}:{os.linesep}'
                f'{os.linesep.join(unimports)}'
            ))
