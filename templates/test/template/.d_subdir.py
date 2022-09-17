import os

from igm.render import download

GITHUB_HOST = os.environ.get('GITHUB_HOST', 'github.com')


def _get_testfile_url(resource, branch='main') -> str:
    if not os.environ.get('NO_GITHUB'):
        return f'https://{GITHUB_HOST}/igm4ai/igm-testfile/raw/{branch}/{resource}'
    else:
        return f'https://gitee.com/hansbug/igm-testfile/raw/{branch}/{resource}'


download(_get_testfile_url('gztar_template-simple.tar.gz'), subdir='template')
