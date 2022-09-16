import pytest
from hbutils.testing import TextAligner
from potc.testing import mock_potc_plugins


@pytest.fixture(autouse=True)
def no_potc_plugins():
    with mock_potc_plugins(clear=True):
        yield


@pytest.fixture()
def text_align() -> TextAligner:
    return TextAligner().multiple_lines()


@pytest.fixture()
def text_align_no_empty(text_align) -> TextAligner:
    return text_align.ls_trans(lambda x: filter(bool, x))
