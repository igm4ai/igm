import builtins
import sys
from functools import partial


class IGMSession:
    def __init__(self, title, version, description, path, template_dir):
        self.__title = title
        self.__version = version
        self.__description = description

        self.__path = path
        self.__template_dir = template_dir

    @property
    def title(self):
        return self.__title

    @property
    def version(self):
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def path(self) -> str:
        return self.__path

    @property
    def template_dir(self) -> str:
        return self.__template_dir

    def print_info(self, file=sys.stdout):
        # print is replaced here to print all the output to ``file``
        # noinspection PyShadowingBuiltins
        print = partial(builtins.print, file=file)

        print(f'{self.__title}, v{self.__version}')
        print(f'{self.__description}')
        print(f'Located at {self.__path!r}.')

    def _python_path(self):
        oldpath = sys.path
        pass
