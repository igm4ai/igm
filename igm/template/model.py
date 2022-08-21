import builtins
from contextlib import contextmanager
from functools import partial

from ..utils import with_pythonpath, normpath


class IGMTemplate:
    def __init__(self, title, version, description,
                 path, template_dir='template'):
        self.__title = title
        self.__version = version
        self.__description = description

        self.__path = normpath(path)
        self.__template_dir = template_dir

    @property
    def title(self):
        return self.__title

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

        print(f'{self.__title}, v{self.__version}')
        print(f'{self.__description}')
        print(f'Located at {self.__path!r}.')

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {self.__title}, v{self.__version}>'

    @contextmanager
    def _python_path(self):
        with with_pythonpath(self.__path):
            yield
