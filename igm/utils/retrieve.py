import contextlib
import mimetypes
import os
import shutil
import tempfile
from typing import Optional
from urllib.request import urlretrieve

from hbutils.system import copy
from pip._internal.models.link import Link

from .archive import unpack_archive
from .vcs import is_vcs_url, retrieve_from_vcs


def _guess_extract_type(filename: str, content: Optional[str] = None) -> Optional[str]:
    if content:
        ext_guess = mimetypes.guess_extension(content)
        if ext_guess:
            for name, exts, _ in shutil.get_unpack_formats():
                if ext_guess in exts:
                    return name

    filename = os.path.normcase(filename)
    for name, exts, _ in shutil.get_unpack_formats():
        for ext in exts:
            if filename.endswith(ext):
                return name

    return content


DOWNLOADABLE_SCHEMES = ['http', 'https', 'ftp']


class InvalidURLScheme(Exception):
    pass


def retrieve_to_local(srcpos, dstpath, auto_unpack: bool = True) -> str:
    if is_vcs_url(srcpos):
        return retrieve_from_vcs(srcpos, dstpath)
    else:
        link = Link(srcpos)
        if not link.is_file and link.scheme:  # is a url
            if link.scheme in DOWNLOADABLE_SCHEMES:  # is http/https/ftp url
                filename = link.filename
                with tempfile.TemporaryDirectory() as tdir:
                    local_filename, headers = urlretrieve(srcpos, os.path.join(tdir, filename))
                    archive_format = _guess_extract_type(filename, headers.get('Content-Type', None))
                    if auto_unpack and archive_format:  # unpack archive file to directory
                        unpack_archive(local_filename, dstpath, archive_format)
                        return dstpath
                    else:  # just copy the file
                        copy(local_filename, dstpath)
                        return dstpath

            else:  # unknown url
                raise InvalidURLScheme(link)

        else:  # is a local file
            filedir, filename = os.path.split(dstpath)
            archive_format = _guess_extract_type(filename)
            if auto_unpack and archive_format and os.path.isfile(srcpos):  # is an archive file
                unpack_archive(srcpos, dstpath, archive_format)
                return dstpath
            else:  # just copy the file
                copy(srcpos, dstpath)
                return dstpath


@contextlib.contextmanager
def retrieve(srcpos, auto_unpack: bool = True) -> str:
    with tempfile.TemporaryDirectory() as td:
        target = os.path.join(td, Link(srcpos).filename)
        downloaded = retrieve_to_local(srcpos, target, auto_unpack=auto_unpack)
        yield os.path.join(downloaded)
