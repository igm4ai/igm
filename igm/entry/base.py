import builtins
import itertools
import os
import traceback
from functools import wraps, partial
from typing import Optional, IO, Callable

import click
from click.exceptions import ClickException

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


class ClickWarningException(ClickException):
    def show(self, file: Optional[IO] = None) -> None:
        click.secho(self.format_message(), fg='yellow')


class ClickErrorException(ClickException):
    def show(self, file: Optional[IO] = None) -> None:
        click.secho(self.format_message(), fg='red')


# noinspection PyShadowingBuiltins
def print_exception(err: BaseException, print: Optional[Callable] = None):
    # noinspection PyShadowingBuiltins
    print = print or builtins.print

    lines = list(itertools.chain(*map(
        lambda x: x.splitlines(keepends=False),
        traceback.format_tb(err.__traceback__)
    )))

    if lines:
        print('Traceback (most recent call last):')
        print(os.linesep.join(lines))

    if len(err.args) == 0:
        print(f'{type(err).__name__}')
    elif len(err.args) == 1:
        print(f'{type(err).__name__}: {err.args[0]}')
    else:
        print(f'{type(err).__name__}: {err.args}')


def command_wrap():
    def _decorator(func):
        @wraps(func)
        def _new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ClickException:
                raise
            except BaseException as err:
                click.secho('Unexpected error found when running IGM CLI!', fg='red')
                print_exception(err, partial(click.secho, fg='red'))

        return _new_func

    return _decorator
