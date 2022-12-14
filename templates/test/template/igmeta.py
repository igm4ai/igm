import sys

from igm.conf import igm_project, cpy, cpip, cmds


def _my_func():
    print('This is my func')


def _another_func():
    """This is another custom function"""
    print('nuts?', file=sys.stderr)


def e1():
    raise ValueError


def e2():
    raise KeyError('key error')


def e3():
    raise TypeError('type', 'error', 233)


def ki():
    raise KeyboardInterrupt


igm_project(
    name={{(user.name | str + '-demo') | potc}},
    version='0.3.2',
    template_name={{template.name | potc}},
    template_version={{template.version | potc}},
    created_at={{py.time.time() | trepr | potc}},
    scripts={
        None: cpy('main.py'),
        'install': cpip('install', '-r', 'requirements.txt'),
        'func': _my_func,
        'func2': _another_func,
        'echo': 'echo {{ py.os.cpu_count() }} cpus',
        'echox': ['echo', '1', '2', '3', '4'],
        'multi': [
            _my_func,
            'echo 233',
            cpy('-V'),
        ],
        'multi2': cmds(
            'This is a complex operation',
            [
                _my_func,
                'echo 233'
            ]
        ),
        'e1': e1,
        'e2': e2,
        'e3': e3,
        'ki': ki,
    }
)
