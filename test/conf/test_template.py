import io
import os.path
import pathlib
from textwrap import dedent
from unittest.mock import patch

import pytest
from hbutils.testing import capture_output, isolated_directory

from igm.conf import IGMTemplate
from igm.utils import normpath
from ..testings import assert_same_path, get_testfile_path


@pytest.mark.unittest
class TestConfTemplate:
    def test_igm_template_base(self):
        template = IGMTemplate('mt', '0.5.4', 'My Template', os.path.join('test', 'utils'))
        assert template.name == 'mt'
        assert template.version == '0.5.4'
        assert template.description == 'My Template'

        assert_same_path(template.path, os.path.join('test', 'utils'))
        assert_same_path(template.template_dir, os.path.join(template.path, 'template'))

        with capture_output() as c:
            template.print_info()
        assert c.stdout.strip() == dedent(f"""
mt, v0.5.4
My Template
Located at {normpath('test/utils')!r}.
        """.strip())

        with io.StringIO() as sf:
            template.print_info(sf)
            assert sf.getvalue().strip() == dedent(f"""
mt, v0.5.4
My Template
Located at {normpath('test/utils')!r}.
            """.strip())

        assert repr(template) == '<IGMTemplate mt, v0.5.4>'

    def test_template_run(self, test_template, text_align_no_empty):
        with isolated_directory():
            test_template.run('project', silent=True)

            assert os.path.exists('project')
            assert os.path.isdir('project')
            assert os.path.exists('project/README.md')
            assert os.path.exists('project/igmeta.py')

            text_align_no_empty.assert_equal(pathlib.Path('project/main.py').read_text(), [
                'cpus = 6',
                "mem_size = '63.76 GiB'",
                "os = 'Windows'",
                "python = 'PyPy 3.7.12'",

                "print('This is your first try!')",
                "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')"
            ])

            text_align_no_empty.assert_equal(pathlib.Path('project/.main.py').read_text(), [
                'cpus = 6',
                "mem_size = '63.76 GiB'",
                "os = 'Windows'",
                "python = 'PyPy 3.7.12'",

                "print('This is your first try!')",
                "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')"
            ])

            text_align_no_empty.assert_equal(pathlib.Path('project/README.md').read_text(), [
                '# hello world for hansbug',
                "This is a hello world project of igm created by 'hansbug' (age: `18`).",

                'You can start this project by the following command:',
                '```python',
                'python main.py',
                '```'
            ])

            text_align_no_empty.assert_equal(pathlib.Path('project/nested/1/2/3/main.py').read_text(), [
                'cpus = 6',
                "mem_size = '63.76 GiB'",
                "os = 'Windows'",
                "python = 'PyPy 3.7.12'",

                "print('This is your first try!')",
                "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')"
            ])

            assert os.path.exists('project/raw.tar.gz')
            assert os.path.isfile('project/raw.tar.gz')
            assert pathlib.Path('project/raw.tar.gz').read_bytes() == \
                   pathlib.Path(get_testfile_path('gztar_template-simple.tar.gz')).read_bytes()

            assert os.path.exists('project/unpacked')
            assert os.path.isdir('project/unpacked')
            assert os.path.exists('project/unpacked/README.md')
            assert os.path.exists('project/unpacked/meta.py')

            assert os.path.exists('project/d_origin.tar.gz')
            assert os.path.isfile('project/d_origin.tar.gz')
            assert pathlib.Path('project/d_origin.tar.gz').read_bytes() == \
                   pathlib.Path(get_testfile_path('gztar_template-simple.tar.gz')).read_bytes()

            assert os.path.exists('project/d_unpacked')
            assert os.path.isdir('project/d_unpacked')
            assert os.path.exists('project/d_unpacked/README.md')
            assert os.path.exists('project/d_unpacked/meta.py')

            assert os.path.exists('project/d_subdir')
            assert os.path.isdir('project/d_subdir')
            assert os.path.exists('project/d_subdir/README.md')
            assert os.path.exists('project/d_subdir/igmeta.py')

            assert os.path.exists('project/script_1.ini')
            assert os.path.isfile('project/script_1.ini')
            assert pathlib.Path('project/script_1.ini').read_text().strip() == 'this is one'

            assert os.path.exists('project/script_2.txt')
            assert os.path.isfile('project/script_2.txt')
            lines = text_align_no_empty.splitlines(pathlib.Path('project/script_2.txt').read_text())
            line1, line2, line3, line4, line5, line6 = lines
            assert line1 == 'this is two'
            assert_same_path(os.path.join('project', line2), 'project/script')
            assert line3 == 'wtf: 103 + 279 = 382'
            assert line4 == '[\'project_dir\', \'template\', \'trepr\', \'wtf\']'
            assert_same_path(line5, 'project')
            assert line6 == str(os.path.getsize('project/script_1.ini'))

            assert os.path.exists('project/nested/1/2/4/script_1.ini')
            assert os.path.isfile('project/nested/1/2/4/script_1.ini')
            assert pathlib.Path('project/nested/1/2/4/script_1.ini').read_text().strip() == 'this is one'

            assert os.path.exists('project/nested/1/2/4/script_2.txt')
            assert os.path.isfile('project/nested/1/2/4/script_2.txt')
            lines = text_align_no_empty.splitlines(
                pathlib.Path('project/nested/1/2/4/script_2.txt').read_text())
            line1, line2, line3, line4, line5 = lines
            assert line1 == 'this is two'
            assert_same_path(os.path.join('project', line2), 'project/script')
            assert line3 == 'wtf: 103 + 279 = 382'
            assert line4 == '[\'project_dir\', \'template\', \'trepr\', \'wtf\']'
            assert line5 == str(os.path.getsize('project/nested/1/2/4/script_1.ini'))

            assert os.path.exists('project/nested/1/2/5/d_unpacked')
            assert os.path.isdir('project/nested/1/2/5/d_unpacked')
            assert os.path.exists('project/nested/1/2/5/d_unpacked/README.md')
            assert os.path.exists('project/nested/1/2/5/d_unpacked/meta.py')

    def test_template_run_error(self, test_template):
        with isolated_directory(), patch.dict('os.environ', {'MAKE_ERROR': '1'}, clear=False):
            with pytest.raises(ValueError):
                test_template.run('project', silent=True)

    def test_template_run_exists(self, test_template):
        with isolated_directory():
            os.makedirs('project', exist_ok=True)
            with pytest.raises(FileExistsError):
                test_template.run('project', silent=True)
