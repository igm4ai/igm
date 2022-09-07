from unittest.mock import patch, MagicMock

import pytest
from easydict import EasyDict
from hbutils.testing import isolated_directory, capture_output

from igm.conf.inquire import with_user_inquire
from igm.render.template import TemplateJob, TemplateImportWarning, IGMRenderTask
from ..testings import CPU_INFO_1, MEMORY_INFO_2, CPU_INFO_100, MEMORY_INFO_100, TWO_GPU_DATA


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
    def test_job_cfg_1(self, config_1):
        with isolated_directory({'template.py': 'templates/simple/template/main.py'}):
            t = TemplateJob('template.py', 'main.py')
            t.run(silent=True)
            with open('main.py', 'r') as rf:
                lines = list(filter(bool, map(str.strip, rf.readlines())))
                assert lines == [
                    'cpus = 6',
                    "mem_size = '63.76 GiB'",
                    "os = 'Windows'",
                    "python = 'PyPy 3.7.12'",

                    "print('This is your first try!')",
                    "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')"
                ]

    def test_job_cfg_2(self, config_2):
        with isolated_directory({'template.py': 'templates/simple/template/main.py'}):
            t = TemplateJob('template.py', 'main.py')
            t.run(silent=True)
            with open('main.py', 'r') as rf:
                lines = list(filter(bool, map(str.strip, rf.readlines())))
                assert lines == [
                    'cpus = 112',
                    "mem_size = '944.35 GiB'",
                    "os = 'macOS'",
                    "python = 'CPython 3.9.4'",
                    "cuda_version = '11.2'",
                    'gpu_num = 2',

                    "print('This is your first try!')",
                    "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')",
                    "print(f'CUDA {cuda_version} is also detected, with {gpu_num} gpu(s).')"
                ]

    def test_task_simple(self, config_2):
        with capture_output() as co:
            with with_user_inquire({'name': 'hansbug', 'age': 24, 'gender': 'Male'}):
                with isolated_directory({'template': 'templates/simple/template'}):
                    t = IGMRenderTask('template', 'project')
                    assert len(t) == 2
                    t.run()

                    with open('project/main.py', 'r') as rf:
                        lines = list(filter(bool, map(str.strip, rf.readlines())))
                        assert lines == [
                            'cpus = 112',
                            "mem_size = '944.35 GiB'",
                            "os = 'macOS'",
                            "python = 'CPython 3.9.4'",
                            "cuda_version = '11.2'",
                            'gpu_num = 2',

                            "print('This is your first try!')",
                            "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')",
                            "print(f'CUDA {cuda_version} is also detected, with {gpu_num} gpu(s).')"
                        ]

                    with open('project/README.md', 'r') as rf:
                        lines = list(filter(bool, map(str.strip, rf.readlines())))
                        assert lines == [
                            '# hello world for hansbug',
                            'This is a hello world project of igm created by \'hansbug\' (age: `24`).',
                            'You can start this project by the following command:',
                            '```python',
                            'python main.py',
                            '```'
                        ]

    def test_task_simple_with_easydict(self, config_2):
        with capture_output() as co:
            with with_user_inquire({'name': EasyDict({'v': 'hansbug'}), 'age': 24, 'gender': 'Male'}):
                with isolated_directory({'template': 'templates/simple/template'}):
                    t = IGMRenderTask('template', 'project')
                    assert len(t) == 2
                    with pytest.warns(TemplateImportWarning):
                        t.run()

                    with open('project/main.py', 'r') as rf:
                        lines = list(filter(bool, map(str.strip, rf.readlines())))
                        assert lines == [
                            'cpus = 112',
                            "mem_size = '944.35 GiB'",
                            "os = 'macOS'",
                            "python = 'CPython 3.9.4'",
                            "cuda_version = '11.2'",
                            'gpu_num = 2',

                            "print('This is your first try!')",
                            "print(f'UR running {python} on {os}, with a {cpus} core {mem_size} device.')",
                            "print(f'CUDA {cuda_version} is also detected, with {gpu_num} gpu(s).')"
                        ]

                    with open('project/README.md', 'r') as rf:
                        lines = list(filter(bool, map(str.strip, rf.readlines())))
                        assert lines == [
                            "# hello world for {'v': 'hansbug'}",
                            "This is a hello world project of igm created by EasyDict({'v': 'hansbug'}) (age: `24`).",
                            'You can start this project by the following command:',
                            '```python',
                            'python main.py',
                            '```'
                        ]
