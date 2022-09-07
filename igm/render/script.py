import os
import shutil
from contextlib import contextmanager
from typing import Optional, Mapping, Any, ContextManager, Tuple
from urllib.request import urlretrieve

from hbutils.reflection import dynamic_call
from hbutils.system import copy

from .base import RenderJob
from ..utils import tqdm_ncols, get_globals, get_url_filename, get_archive_type, get_url_ext
from ..utils.retrieve import TqdmForURLDownload, LocalTemporaryDirectory

_SCRIPT_TAG = '__script__'


def _script_append(script, append):
    def __script__(src, dst, **kwargs):
        if script is not None:
            dynamic_call(script)(src, dst, **kwargs)
        dynamic_call(append)(src, dst, **kwargs)

    return __script__


@contextmanager
def _download_to_temp(url, silent: bool = False) -> ContextManager[Tuple[str, Optional[str]]]:
    filename = get_url_filename(url)
    with LocalTemporaryDirectory() as tdir:
        dstfile = os.path.join(tdir, filename)
        if not silent:
            with TqdmForURLDownload(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                                    ncols=tqdm_ncols(), leave=True) as t:
                local_filename, headers = urlretrieve(url, dstfile, reporthook=t.update_to, data=None)
                t.total = t.n
        else:
            local_filename, headers = urlretrieve(url, dstfile)

        yield dstfile, headers.get('Content-Type', None)


def download(url, auto_unpack: bool = True):
    def _download_file(src, dst, silent: bool = False):
        path, fname = os.path.split(dst)
        with _download_to_temp(url, silent=silent) as (tfile, content_type):
            _archive_type = get_archive_type(get_url_filename(url, content_type), content_type)
            if auto_unpack and _archive_type:
                os.makedirs(dst, exist_ok=True)
                shutil.unpack_archive(tfile, dst, _archive_type)
            else:
                _ext = get_url_ext(url, content_type)
                if _ext and not os.path.normcase(fname).endswith(_ext):
                    fname = f'{fname}{_ext}'

                copy(tfile, os.path.join(path, fname))

    g = get_globals()
    g[_SCRIPT_TAG] = _script_append(g.get(_SCRIPT_TAG, None), _download_file)


def igm_script(func):
    g = get_globals()
    g[_SCRIPT_TAG] = _script_append(g.get(_SCRIPT_TAG, None), func)
    return func


class ScriptJob(RenderJob):
    def __init__(self, srcpath: str, dstpath: str, extras: Optional[Mapping[str, Any]] = None):
        RenderJob.__init__(self, srcpath, dstpath)
        self.__extras = dict(extras or {})

    def run(self, silent: bool = False):
        meta = {}
        with open(self.srcpath, 'r', encoding='utf-8') as f:
            exec(f.read(), meta)

        script = meta.get(_SCRIPT_TAG, None)
        if script:
            script(self.srcpath, self.dstpath, silent=silent, **self.__extras)
