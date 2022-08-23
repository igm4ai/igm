import os.path


def normpath(path: str, *paths: str) -> str:
    """
    Overview:
        Normalize the path to a unique format which is comparable by ``==``.

    :param path: First path segment.
    :param paths: Following segments.
    :return: Full absolute path.
    """
    return os.path.normcase(os.path.normpath(
        os.path.abspath(os.path.join(path, *paths))
    ))
