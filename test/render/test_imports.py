import os

import pytest

from igm.render.imports import PyImport


@pytest.fixture()
def py():
    return PyImport()


@pytest.mark.unittest
class TestRenderImports:
    def test_import_getattr(self, py):
        assert py.os is os
        assert py.os.cpu_count() == os.cpu_count()
        assert py.os.path.abspath('111') == os.path.abspath('111')

    def test_import_getitem(self, py):
        assert py['os'] is os
        assert py['os.cpu_count'] is os.cpu_count
        assert py['os.cpu_count']() == os.cpu_count()

    def test_import_repr(self, py):
        assert repr(py) == '<PyImport>'
