import sys
from contextlib import contextmanager


@contextmanager
def with_pythonpath(*path, recover=True, recover_when_replaced=False):
    """
    Overview:
        Append ``PYTHONPATH`` in context, the packages in given paths will be able to be imported.

    :param path: Appended python path.
    :param recover: Recover the ``sys.path`` when context is over, default is ``True``.
    :param recover_when_replaced: If ``sys.path`` is replaced again, recover it or not, default is ``False``.
    """

    oldpath = sys.path
    newpath = [*path, *oldpath]

    try:
        sys.path = newpath
        yield
    finally:
        if recover and (sys.path is newpath or recover_when_replaced):
            sys.path = oldpath
