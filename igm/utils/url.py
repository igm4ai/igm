import mimetypes
import os.path
from itertools import chain
from typing import Optional
from urllib.parse import urlparse, unquote


def get_url_filename(url: str, content_type: Optional[str] = None) -> str:
    """
    Overview:
        Get filename from ``url`` and ``content_type``.

    :param url: Original url.
    :param content_type: Content-Type information from remote.
    :return: Filename with correct extension name.
    """
    url_parsed = urlparse(url)
    filename = os.path.basename(unquote(url_parsed.path))
    if content_type:
        actual_ext = mimetypes.guess_extension(content_type)
        if actual_ext and not os.path.normcase(filename).endswith(actual_ext):
            filename = f'{filename}{actual_ext}'

    return filename


def _iter_extensions():
    for n1, n2 in chain(*map(
            lambda x: x.items(),
            [mimetypes.types_map, mimetypes.common_types, mimetypes.encodings_map, mimetypes.suffix_map]
    )):
        if n1.startswith('.'):
            yield n1
        if n2.startswith('.'):
            yield n2


def get_url_ext(url: str, content_type: Optional[str] = None) -> str:
    """
    Overview:
        Get extension of url, based on url filename and content type.

    :param url: Original url.
    :param content_type: Content-Type information from remote.
    :return: File extension, including ``.tar.gz``.
    """
    filename = get_url_filename(url, content_type)
    filename = os.path.normcase(filename)
    ext = ''
    for exist_ext in _iter_extensions():
        if filename.endswith(exist_ext) and len(exist_ext) > len(ext):
            ext = exist_ext

    if not ext:
        _, ext = os.path.splitext(filename)

    return ext
