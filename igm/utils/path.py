import os.path


def get_file_ext(file: str) -> str:
    """

    :param file:
    :return:
    """
    _, ext = os.path.splitext(os.path.normcase(file))
    return ext


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
