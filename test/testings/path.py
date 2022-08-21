import os.path


def _normpath(path) -> str:
    return os.path.normcase(os.path.normpath(os.path.abspath(path)))


def assert_same_path(path1, path2, msg=None):
    assert _normpath(path1) == _normpath(path2), \
        msg or f'{path1!r} is not equal to {path2!r}.'
