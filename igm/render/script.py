import os
import shutil
from contextlib import contextmanager
from functools import wraps
from typing import Optional, Mapping, Any, ContextManager, Tuple
from urllib.request import urlretrieve

from hbutils.reflection import dynamic_call

from .base import RenderJob
from ..utils import tqdm_ncols, get_globals, get_url_filename, get_archive_type, get_url_ext
from ..utils.retrieve import TqdmForURLDownload, LocalTemporaryDirectory

_SCRIPT_TAG = '__script__'


def _script_append(script, append):
    def __script__(dst, **kwargs):
        if script is not None:
            dynamic_call(script)(dst, **kwargs)
        dynamic_call(append)(dst, **kwargs)

    return __script__


def igm_script_build(func):
    @wraps(func)
    def _new_func(*args, **kwargs):
        g = get_globals()
        _method = func(*args, **kwargs)
        g[_SCRIPT_TAG] = _script_append(g.get(_SCRIPT_TAG, None), _method)
        return _method

    return _new_func


def igm_script(func):
    g = get_globals()
    g[_SCRIPT_TAG] = _script_append(g.get(_SCRIPT_TAG, None), func)
    return func


@contextmanager
def _download_to_temp(url) -> ContextManager[Tuple[str, Optional[str]]]:
    filename = get_url_filename(url)
    with LocalTemporaryDirectory() as tdir:
        dstfile = os.path.join(tdir, filename)
        with TqdmForURLDownload(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                                ncols=tqdm_ncols(), leave=True) as t:
            local_filename, headers = urlretrieve(url, dstfile, reporthook=t.update_to, data=None)
            t.total = t.n

        yield dstfile, headers.get('Content-Type', None)


@igm_script_build
def download(url, auto_unpack: bool = True):
    def _download_file(dst):
        path, fname = os.path.split(dst)
        with _download_to_temp(url) as (tfile, content_type):
            _archive_type = get_archive_type(get_url_filename(url, content_type), content_type)
            if auto_unpack and _archive_type:
                os.makedirs(dst, exist_ok=True)
                shutil.unpack_archive(tfile, dst, _archive_type)
            else:
                _ext = get_url_ext(url, content_type)
                if _ext and not os.path.normcase(fname).endswith(_ext):
                    fname = f'{fname}{_ext}'
                shutil.move(tfile, os.path.join(path, fname))

    return _download_file


class ScriptJob(RenderJob):
    def __init__(self, srcpath: str, dstpath: str, extras: Optional[Mapping[str, Any]] = None):
        RenderJob.__init__(self, srcpath, dstpath)
        self.__extras = dict(extras or {})

    def _run(self):
        meta = {}
        with open(self.srcpath, 'r', encoding='utf-8') as f:
            exec(f.read(), meta)

        script = meta.get(_SCRIPT_TAG, None)
        if script:
            abs_dstpath = os.path.abspath(self.dstpath)
            dstdir, dstfile = os.path.split(abs_dstpath)
            curdir = os.path.abspath(os.curdir)

            try:
                rel_dstpath = os.path.relpath(abs_dstpath, start=dstdir)
                os.chdir(dstdir)
                script(rel_dstpath, **self.__extras)
            finally:
                os.chdir(curdir)
