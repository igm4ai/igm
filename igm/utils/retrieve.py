import contextlib
import mimetypes
import os
import tempfile
from urllib.request import urlretrieve

from hbutils.system import copy
from pip._internal.models.link import Link

from .archive import unpack_archive, _get_format_by_extension
from .vcs import is_vcs_url, retrieve_from_vcs

HTTP_SCHEME = ['http', 'https']


class InvalidURL(Exception):
    pass


def retrieve_to_local(srcpos, dstpath, use_link: bool = False, auto_unpack: bool = True) -> str:
    if is_vcs_url(srcpos):
        return retrieve_from_vcs(srcpos, dstpath)
    else:
        link = Link(srcpos)
        if link.scheme:
            if link.scheme in HTTP_SCHEME:  # is http url
                filename = link.filename
                with tempfile.TemporaryDirectory() as tdir:
                    local_filename, headers = urlretrieve(srcpos, os.path.join(tdir, filename))
                    if auto_unpack:  # unpack zip to directory
                        content_type = headers.get('Content-Type', None)
                        guessed_extension = mimetypes.guess_extension(content_type)
                        if content_type and guessed_extension:
                            fmt = _get_format_by_extension(guessed_extension)
                        else:
                            fmt = None

                        unpack_archive(local_filename, dstpath, fmt)
                        return dstpath

                    else:  # just copy the file
                        copy(local_filename, dstpath)
                        return dstpath

            else:
                raise InvalidURL(link)

        else:  # is a local file
            filedir, filename = os.path.split(dstpath)
            if not os.path.exists(filedir):
                os.makedirs(filedir, exist_ok=True)
            if not use_link:  # mave a copy to target
                copy(srcpos, dstpath)
                return dstpath
            else:  # create a link anchored to srcpos
                os.symlink(srcpos, dstpath, target_is_directory=os.path.isdir(srcpos))
                return dstpath


@contextlib.contextmanager
def retrieve(srcpos, *subdir, auto_unpack: bool = True) -> str:
    with tempfile.TemporaryDirectory() as td:
        target = os.path.join(td, Link(srcpos).filename)
        downloaded = retrieve_to_local(srcpos, target, use_link=False, auto_unpack=auto_unpack)
        yield os.path.join(downloaded, *subdir)
