import os.path

from .env import GITHUB_HOST, _has_github


def get_testfile_url(resource: str, branch: str = 'main'):
    if _has_github():
        return f'https://{GITHUB_HOST}/igm4ai/igm-testfile/raw/{branch}/{resource}'
    else:
        return f'https://gitee.com/hansbug/igm-testfile/raw/{branch}/{resource}'


_LOCAL_DIR, _ = os.path.split(os.path.abspath(__file__))


def get_testfile_path(path: str) -> str:
    return os.path.normpath(os.path.join(_LOCAL_DIR, '..', 'testfile', path))
