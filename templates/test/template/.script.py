import os

from igm.render import igm_script


@igm_script
def run1(dst):
    with open('script_1.ini', 'w') as f:
        print('this is one', file=f)


@igm_script
def run2(dst):
    with open('script_2.txt', 'w') as f:
        print('this is two', file=f)
        print(dst, file=f)
        print(os.path.getsize('script_1.ini'), file=f)


@igm_script
def err(dst):
    if os.environ.get('MAKE_ERROR'):
        raise ValueError('This is the error')
