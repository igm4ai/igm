import os.path
import sys
from unittest import skipUnless

import pytest
from hbutils.testing import isolated_directory, isolated_stdin, capture_output

from igm.conf.project import load_igm_project, IGMProject, NotIGMProject, IGMCommandScript, IGMFuncScript, IGMScriptSet
from ..testings import TEMPLATE_SIMPLE_VERSION, TEMPLATE_TEST_VERSION


@pytest.mark.unittest
class TestConfProject:
    def test_load_igm_project_simple(self, simple_project):
        with load_igm_project(simple_project) as p:
            assert isinstance(p, IGMProject)
            assert p.name == 'hansbug-simple-demo'
            assert p.version == '0.3.2'
            assert p.template_name == 'simple'
            assert p.template_version == TEMPLATE_SIMPLE_VERSION

            assert set(p.scripts.keys()) == {None}
            assert None in p.scripts
            assert isinstance(p.scripts[None], IGMCommandScript)
            assert p.scripts[None].args == [sys.executable, 'main.py']
            assert p.scripts[None].describe() == 'Command - python main.py'

            with isolated_directory():
                with open('main.py', 'w') as f:
                    f.write('print("this is main.py")\n')
                    f.write('import time\n')
                    f.write('time.sleep(1)\n')
                    f.write('print("this is main.py x")\n')
                    f.write('t = input()\n')
                    f.write('print("this is main.py 233", t, t)\n')

                with isolated_stdin(['input_text']):
                    with capture_output() as co:
                        p.scripts[None].run()

                lines = list(filter(bool, map(str.strip, co.stdout.splitlines())))
                assert 'main.py' in lines[0]
                assert 'python' in lines[0]
                assert lines[1:] == [
                    f'this is main.py',
                    f'this is main.py x',
                    f'this is main.py 233 input_text input_text'
                ]

    def test_load_igm_project_simple_with_file(self, simple_project):
        with load_igm_project(os.path.join(simple_project, 'igmeta.py')) as p:
            assert isinstance(p, IGMProject)
            assert p.name == 'hansbug-simple-demo'
            assert p.version == '0.3.2'
            assert p.template_name == 'simple'
            assert p.template_version == TEMPLATE_SIMPLE_VERSION

    def test_load_igm_project_test(self, test_project):
        with load_igm_project(test_project) as p:
            assert isinstance(p, IGMProject)
            assert p.name == 'hansbug-demo'
            assert p.version == '0.3.2'
            assert p.template_name == 'test'
            assert p.template_version == TEMPLATE_TEST_VERSION

            none = p.scripts[None]
            assert isinstance(none, IGMCommandScript)
            assert none.args == [sys.executable, 'main.py']
            assert none.describe() == 'Command - python main.py'

            install = p.scripts['install']
            assert isinstance(install, IGMCommandScript)
            assert install.args == [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']
            assert install.describe() == 'Command - pip install -r requirements.txt'

            func = p.scripts['func']
            assert isinstance(func, IGMFuncScript)
            assert func.describe() == 'Call function \'_my_func\'.'
            with capture_output() as co:
                func.run()
            assert co.stdout.strip() == 'This is my func'
            assert co.stderr.strip() == ''

            func2 = p.scripts['func2']
            assert isinstance(func2, IGMFuncScript)
            assert func2.describe() == 'This is another custom function'
            with capture_output() as co:
                func2.run()
            assert co.stdout.strip() == ''
            assert co.stderr.strip() == 'nuts?'

            echo = p.scripts['echo']
            assert isinstance(echo, IGMCommandScript)
            assert echo.args == ['echo', str(os.cpu_count()), 'cpus']
            assert echo.describe() == f'Command - echo {os.cpu_count()} cpus'
            with capture_output() as co:
                echo.run()
            assert co.stdout.strip().splitlines(keepends=False) == [
                f'echo {os.cpu_count()} cpus',
                f'{os.cpu_count()} cpus'
            ]
            assert co.stderr.strip() == ''

            echox = p.scripts['echox']
            assert isinstance(echox, IGMCommandScript)
            assert echox.args == ['echo', '1', '2', '3', '4']
            assert echox.describe() == 'Command - echo 1 2 3 4'
            with capture_output() as co:
                echox.run()
            assert co.stdout.strip().splitlines(keepends=False) == ['echo 1 2 3 4', '1 2 3 4']
            assert co.stderr.strip() == ''

            multi = p.scripts['multi']
            assert isinstance(multi, IGMScriptSet)
            assert len(multi.scripts) == 3
            assert multi.describe() == 'Run a set of 3 scripts in order.'

    @skipUnless(not os.path.exists('/not_found_dir'), 'directory not exist required')
    def test_load_igm_project_not_found(self):
        with pytest.raises(FileNotFoundError):
            with load_igm_project('/not_found_dir'):
                pytest.fail('Should not reach here!')

    def test_load_igm_project_invalid(self):
        with isolated_directory():
            with open('igmeta.py', 'w') as f:
                f.write("""
A = 1
                """)

            with pytest.raises(NotIGMProject):
                with load_igm_project('.'):
                    pytest.fail('Should not reach here!')

            with pytest.raises(NotIGMProject):
                with load_igm_project('igmeta.py'):
                    pytest.fail('Should not reach here!')
