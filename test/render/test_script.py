import os.path
import pathlib
from unittest import skipUnless

import pytest
from hbutils.testing import isolated_directory, capture_output

from igm.render.script import ScriptJob
from test.testings import get_testfile_url


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestRenderScript:
    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    @pytest.mark.parametrize(
        ['fmt', 'ext', 'silent'],
        [
            ('7z', '.7z', True),
            ('rar', '.rar', False),
            ('bztar', '.tar.bz2', True),
            ('gztar', '.tar.gz', False),
            ('tar', '.tar', True),
            ('xztar', '.tar.xz', False),
            ('zip', '.zip', True),
        ]
    )
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    def test_script_download_unpack(self, fmt, ext, silent):
        with capture_output(), isolated_directory():
            with open('script1.py', 'w') as f:
                print(f"""
from igm.render import download
from test.testings import get_testfile_url

download({get_testfile_url(f'{fmt}_template-simple{ext}')!r})
                """, file=f)

            script_file = os.path.abspath('script1.py')
            with isolated_directory():
                job = ScriptJob(script_file, 'main')
                job.run(silent=silent)

                assert os.path.exists('main')
                assert os.path.isdir('main')
                assert not os.path.exists(f'main{ext}')
                assert not os.path.isfile(f'main{ext}')
                assert os.path.exists('main/README.md')
                assert os.path.isfile('main/README.md')
                assert os.path.exists('main/meta.py')
                assert os.path.isfile('main/meta.py')

    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    @pytest.mark.parametrize(
        ['fmt', 'ext', 'silent'],
        [
            ('7z', '.7z', True),
            ('rar', '.rar', False),
            ('bztar', '.tar.bz2', True),
            ('gztar', '.tar.gz', False),
            ('tar', '.tar', True),
            ('xztar', '.tar.xz', False),
            ('zip', '.zip', True),
        ]
    )
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    def test_script_download_not_unpack(self, fmt, ext, silent):
        with capture_output(), isolated_directory():
            with open('script2.py', 'w') as f:
                print(f"""
from igm.render import download
from test.testings import get_testfile_url

download({get_testfile_url(f'{fmt}_template-simple{ext}')!r}, auto_unpack=False)
                """, file=f)

            script_file = os.path.abspath('script2.py')
            with isolated_directory():
                job = ScriptJob(script_file, 'main')
                job.run(silent=silent)

                assert not os.path.exists('main')
                assert not os.path.isdir('main')
                assert os.path.exists(f'main{ext}')
                assert os.path.isfile(f'main{ext}')

    @pytest.mark.parametrize(
        ['a', 'b', 'result'],
        [
            (1, 2, 3),
            (2, 3, 5),
            (5, 7, 12),
        ]
    )
    def test_script_custom(self, a, b, result):
        with capture_output(), isolated_directory():
            with open('script.py', 'w') as f:
                print(f"""
from igm.render import igm_script

@igm_script
def plus_result(dst):
    A = {a}
    B = {b}
    with open(dst, 'w') as f:
        print(f'{{A}} + {{B}} = {{A + B}}', file=f)
                """, file=f)

            script_file = os.path.abspath('script.py')
            with isolated_directory():
                job = ScriptJob(script_file, 'main')
                job.run(silent=True)

                assert os.path.exists('main')
                assert os.path.isfile('main')
                assert pathlib.Path('main').read_text().strip() == f'{a} + {b} = {result}'

    @pytest.mark.flaky(reruns=3, reruns_delay=5)
    @pytest.mark.parametrize(
        ['fmt', 'ext', 'silent'],
        [
            ('bztar', '.tar.bz2', True),
            ('gztar', '.tar.gz', False),
            ('tar', '.tar', True),
            ('xztar', '.tar.xz', False),
            ('zip', '.zip', True),
        ]
    )
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    def test_script_download_chain(self, fmt, ext, silent):
        with capture_output() as co, isolated_directory():
            with open('script.py', 'w') as f:
                print(f"""
import os
from igm.render import download, igm_script
from test.testings import get_testfile_url

download({get_testfile_url(f'{fmt}_template-simple{ext}')!r}, auto_unpack=False)

@igm_script
def size_measure(dst):
    print('This is not silent') 
    with open(dst + '.size', 'w') as f:
        print(os.path.getsize('main{ext}'), file=f)
                """, file=f)

            script_file = os.path.abspath('script.py')
            with isolated_directory():
                job = ScriptJob(script_file, 'main')
                job.run(silent=silent)

                assert not os.path.exists('main')
                assert not os.path.isdir('main')
                assert os.path.exists(f'main{ext}')
                assert os.path.isfile(f'main{ext}')

                assert os.path.exists(f'main.size')
                assert os.path.isfile(f'main.size')
                assert os.path.getsize(f'main.size') > 0

        if silent:
            assert not co.stdout.strip()
        else:
            assert co.stdout.strip()
