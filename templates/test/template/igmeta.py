from igm.conf import igm_project, cpy, cpip


def _my_func():
    print('This is my func')


igm_project(
    name={{ (user.name | str + '-demo') | potc }},
    version='0.3.2',
    template_name={{ template.name | potc }},
    template_version={{ template.version | potc }},
    created_at={{ py.time.time() | potc }},
    scripts={
        None: cpy('main.py'),
        'install': cpip('install', '-r', 'requirements.txt'),
        'func': _my_func,
        'echo': 'echo 1 2 3 4'
    }
)
