import builtins
from functools import partial
from typing import Optional, Callable, Mapping

from .inquire import with_user_inquire, inquire_call
from ..utils import with_pythonpath, normpath

_DEFAULT_TEMPLATE_DIR = 'template'


class IGMTemplate:
    def __init__(self, name, version, description,
                 path, template_dir=_DEFAULT_TEMPLATE_DIR,
                 inquire: Optional[Callable[[], Mapping]] = None):
        self.__name = name
        self.__version = version
        self.__description = description

        self.__path = normpath(path)
        self.__template_dir = normpath(self.__path, template_dir)

        self.__inquire = (inquire or (lambda: {}))

    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version

    @property
    def description(self) -> str:
        return self.__description

    @property
    def path(self) -> str:
        return self.__path

    @property
    def template_dir(self) -> str:
        return self.__template_dir

    def print_info(self, file=None):
        # print is replaced here to print all the output to ``file``
        if file is not None:
            # noinspection PyShadowingBuiltins
            print = partial(builtins.print, file=file)
        else:
            # noinspection PyShadowingBuiltins
            print = builtins.print

        print(f'{self.__name}, v{self.__version}')
        print(f'{self.__description}')
        print(f'Located at {self.__path!r}.')

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {self.__name}, v{self.__version}>'

    def run(self):
        ok, inquire_data = inquire_call(self.__inquire)
        if ok:
            with with_user_inquire(inquire_data), with_pythonpath(self.__path):
                from igm.env import user, env, sys
                print({'user': user, 'env': env, 'sys': sys})
