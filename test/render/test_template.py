import os
import pathlib
from unittest.mock import patch, MagicMock

import pytest
from easydict import EasyDict
from hbutils.testing import isolated_directory, capture_output, tmatrix
from time_machine import travel

from igm.conf.inquire import with_user_inquire
from igm.render.template import TemplateJob, TemplateImportWarning, IGMRenderTask, CopyJob
from ..testings import CPU_INFO_1, MEMORY_INFO_2, CPU_INFO_100, MEMORY_INFO_100, TWO_GPU_DATA, get_testfile_path, \
    assert_same_path, TEMPLATE_SIMPLE_VERSION, TEMPLATE_TEST_VERSION


@pytest.fixture()
def config_1():
    with patch('igm.env.system.get_cpu_info', MagicMock(return_value=CPU_INFO_1)), \
            patch('igm.env.system.get_memory_info', MagicMock(return_value=MEMORY_INFO_2)), \
            patch('platform.python_version', MagicMock(return_value='3.7.12')), \
            patch('platform.python_implementation', MagicMock(return_value='Pypy')), \
            patch('platform.system', MagicMock(return_value='Windows')), \
            patch('igm.env.hardware.nvidia.which', MagicMock(return_value=None)):
        yield


@pytest.fixture()
def config_2():
    with patch('igm.env.system.get_cpu_info', MagicMock(return_value=CPU_INFO_100)), \
            patch('igm.env.system.get_memory_info', MagicMock(return_value=MEMORY_INFO_100)), \
            patch('platform.python_version', MagicMock(return_value='3.9.4')), \
            patch('platform.python_implementation', MagicMock(return_value='CPython')), \
            patch('platform.system', MagicMock(return_value='macos')), \
            patch('igm.env.system.get_nvidia_info', MagicMock(return_value=TWO_GPU_DATA)):
        yield


@pytest.mark.unittest
class TestRenderTemplate:
    def test_job_cfg_1(self, config_1, text_align_no_empty):
        with isolated_directory({'template.py': 'templates/simple/template/main.py'}):
            t = TemplateJob('template.py', 'main.py')
            t.run(silent=True)

            text_align_no_empty.assert_equal(pathlib.Path('main.py').read_text(), [
                'cpus = 6',
                "mem_size = '63.76 GiB'",
                "os = 'Windows'",
                "python = 'PyPy 3.7.12'",

                "print('This is your first try!')",
                "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')"
            ])

    def test_job_cfg_2(self, config_2, text_align_no_empty):
        with isolated_directory({'template.py': 'templates/simple/template/main.py'}):
            t = TemplateJob('template.py', 'main.py')
            t.run(silent=True)

            text_align_no_empty.assert_equal(pathlib.Path('main.py').read_text(), [
                'cpus = 112',
                "mem_size = '944.35 GiB'",
                "os = 'macOS'",
                "python = 'CPython 3.9.4'",
                "cuda_version = '11.2'",
                'gpu_num = 2',

                "print('This is your first try!')",
                "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')",
                "print(f'CUDA {cuda_version} is also detected, with {gpu_num} gpu(s).')"
            ])

    @pytest.mark.parametrize(['silent'], [(True,), (False,)])
    def test_task_simple(self, config_2, silent, text_align_no_empty):
        with capture_output():
            with with_user_inquire({'name': 'hansbug', 'age': 24, 'gender': 'Male'}):
                with isolated_directory({'template': 'templates/simple/template'}):
                    t = IGMRenderTask(
                        'template', 'project',
                        extras=dict(template=EasyDict(name='simple', version=TEMPLATE_SIMPLE_VERSION)),
                    )
                    assert len(t) == 3
                    assert repr(t) == '<IGMRenderTask 3 jobs, srcdir: \'template\'>'
                    t.run(silent=silent)

                    text_align_no_empty.assert_equal(pathlib.Path('project/main.py').read_text(), [
                        'cpus = 112',
                        "mem_size = '944.35 GiB'",
                        "os = 'macOS'",
                        "python = 'CPython 3.9.4'",
                        "cuda_version = '11.2'",
                        'gpu_num = 2',

                        "print('This is your first try!')",
                        "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')",
                        "print(f'CUDA {cuda_version} is also detected, with {gpu_num} gpu(s).')"
                    ])

                    text_align_no_empty.assert_equal(pathlib.Path('project/README.md').read_text(), [
                        '# hello world for hansbug',
                        'This is a hello world project of igm created by \'hansbug\' (age: `24`).',
                        'You can start this project by the following command:',
                        '```shell',
                        'igm run',
                        '```'
                    ])

    @travel(1662714925.0)
    def test_task_simple_with_easydict(self, config_2, text_align_no_empty):
        with capture_output():
            with with_user_inquire({'name': EasyDict({'v': 'hansbug'}), 'age': 24, 'gender': 'Male'}):
                with isolated_directory({'template': 'templates/simple/template'}):
                    t = IGMRenderTask(
                        'template', 'project',
                        extras=dict(template=EasyDict(name='simple', version=TEMPLATE_SIMPLE_VERSION)),
                    )
                    assert len(t) == 3
                    with pytest.warns(TemplateImportWarning):
                        t.run()

                    text_align_no_empty.assert_equal(pathlib.Path('project/main.py').read_text(), [
                        'cpus = 112',
                        "mem_size = '944.35 GiB'",
                        "os = 'macOS'",
                        "python = 'CPython 3.9.4'",
                        "cuda_version = '11.2'",
                        'gpu_num = 2',

                        "print('This is your first try!')",
                        "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')",
                        "print(f'CUDA {cuda_version} is also detected, with {gpu_num} gpu(s).')"
                    ])

                    text_align_no_empty.assert_equal(pathlib.Path('project/README.md').read_text(), [
                        "# hello world for {'v': 'hansbug'}",
                        "This is a hello world project of igm created by EasyDict({'v': 'hansbug'}) (age: `24`).",
                        'You can start this project by the following command:',
                        '```shell',
                        'igm run',
                        '```'
                    ])

                    text_align_no_empty.assert_equal(pathlib.Path('project/igmeta.py').read_text(), [
                        f'from igm.conf import igm_project, cpy',
                        f'igm_project(',
                        '    name="{\'v\': \'hansbug\'}-simple-demo",',
                        f"    version='0.3.2',",
                        f"    template_name='simple',",
                        f"    template_version='{TEMPLATE_SIMPLE_VERSION}',",
                        f'    created_at=1662714925,',
                        r'    scripts={',
                        r"        None: cpy('main.py')",
                        r'    }',
                        r')'
                    ])

    @pytest.mark.parametrize(
        ['fmt', 'ext'],
        [
            ('7z', '.7z'),
            ('rar', '.rar'),
            ('bztar', '.tar.bz2'),
            ('gztar', '.tar.gz'),
            ('tar', '.tar'),
            ('xztar', '.tar.xz'),
            ('zip', '.zip'),
        ]
    )
    def test_copy_job(self, fmt, ext):
        with isolated_directory({f'archive{ext}': get_testfile_path(f'{fmt}_template-simple{ext}')}):
            archive_file = os.path.abspath(f'archive{ext}')
            with isolated_directory():
                job = CopyJob(archive_file, f'main{ext}')
                job.run(silent=True)

                assert os.path.exists(f'main{ext}')
                assert pathlib.Path(archive_file).read_bytes() == \
                       pathlib.Path(f'main{ext}').read_bytes()

    @pytest.mark.parametrize(*tmatrix({'silent': [True, False]}))
    def test_task_test(self, config_2, silent, text_align_no_empty):
        with capture_output():
            with with_user_inquire({'name': 'hansbug', 'age': 24, 'gender': 'Male'}):
                with isolated_directory({'template': 'templates/test/template'}):
                    t = IGMRenderTask(
                        'template', 'project',
                        extras=dict(
                            template=EasyDict(name='test', version=TEMPLATE_TEST_VERSION),
                            trepr=int,
                            wtf=lambda x, y: f'wtf: {x} + {y} = {x + y}',
                            project_dir=os.path.abspath('project'),
                        ),
                    )
                    assert len(t) == 14
                    assert repr(t) == '<IGMRenderTask 14 jobs, srcdir: \'template\'>'
                    t.run(silent=silent)

                    text_align_no_empty.assert_equal(pathlib.Path('project/main.py').read_text(), [
                        'cpus = 112',
                        "mem_size = '944.35 GiB'",
                        "os = 'macOS'",
                        "python = 'CPython 3.9.4'",
                        "cuda_version = '11.2'",
                        'gpu_num = 2',

                        "print('This is your first try!')",
                        "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')",
                        "print(f'CUDA {cuda_version} is also detected, with {gpu_num} gpu(s).')"
                    ])

                    text_align_no_empty.assert_equal(pathlib.Path('project/.main.py').read_text(), [
                        'cpus = 112',
                        "mem_size = '944.35 GiB'",
                        "os = 'macOS'",
                        "python = 'CPython 3.9.4'",
                        "cuda_version = '11.2'",
                        'gpu_num = 2',

                        "print('This is your first try!')",
                        "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')",
                        "print(f'CUDA {cuda_version} is also detected, with {gpu_num} gpu(s).')"
                    ])

                    text_align_no_empty.assert_equal(pathlib.Path('project/README.md').read_text(), [
                        '# hello world for hansbug',
                        'This is a hello world project of igm created by \'hansbug\' (age: `24`).',
                        'You can start this project by the following command:',
                        '```python',
                        'python main.py',
                        '```'
                    ])

                    text_align_no_empty.assert_equal(pathlib.Path('project/nested/1/2/3/main.py').read_text(), [
                        'cpus = 112',
                        "mem_size = '944.35 GiB'",
                        "os = 'macOS'",
                        "python = 'CPython 3.9.4'",
                        "cuda_version = '11.2'",
                        'gpu_num = 2',

                        "print('This is your first try!')",
                        "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')",
                        "print(f'CUDA {cuda_version} is also detected, with {gpu_num} gpu(s).')"
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
