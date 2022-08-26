import platform

import pytest

from igm.env.python import get_python_info, Python, PythonImplement, Pip


@pytest.mark.unittest
class TestEnvPythonPy:
    def test_python_implement(self):
        assert PythonImplement.CPYTHON == PythonImplement.CPYTHON
        assert PythonImplement.CPYTHON == 'cpython'
        assert PythonImplement.CPYTHON == 'CPython'
        assert PythonImplement.CPYTHON != 2
        assert PythonImplement.CPYTHON != None

        assert str(PythonImplement.CPYTHON) == 'CPython'
        assert repr(PythonImplement.CPYTHON) == '<PythonImplement CPython>'

    def test_python_info_actual(self):
        python = Python(get_python_info())
        assert python.version == platform.python_version()
        assert python.version == python.version
        assert python.version != 2
        assert python.version != None

        assert python.implement == platform.python_implementation()
        assert python.implement == python.implement
        assert python.implement != 2
        assert python.implement != None

        assert isinstance(python.pip, Pip)

    def test_cpython_3_7_12(self, cpython_3_7_12):
        python = Python(get_python_info())
        assert python.version == '3.7.12'
        assert python.implement == 'cpython'
        assert str(python) == 'CPython 3.7.12'
        assert repr(python) == '<Python, version: 3.7.12, implement: CPython>'

    def test_pypy_3_9_2(self, pypy_3_9_2):
        python = Python(get_python_info())
        assert python.version == '3.9.2'
        assert python.implement == 'pypy'
        assert str(python) == 'PyPy 3.9.2'
        assert repr(python) == '<Python, version: 3.9.2, implement: PyPy>'
