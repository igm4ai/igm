import os
import shlex
from contextlib import contextmanager
from unittest.mock import patch

import pytest


@pytest.fixture()
def mock_argv(args):
    if isinstance(args, str):
        args = shlex.split(args)

    with patch('sys.argv', args):
        yield


@pytest.fixture()
def mock_exitcode():
    def _fake_func(x=None):
        raise SystemExit(x or 0)

    _exitcode = None

    def _get_exitcode():
        return _exitcode

    @contextmanager
    def _mocker():
        try:
            with patch('sys.exit', _fake_func):
                yield _get_exitcode
        except SystemExit as err:
            nonlocal _exitcode
            _exitcode = err.code

    return _mocker
