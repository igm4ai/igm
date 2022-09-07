import pytest
from potc.testing import mock_potc_plugins


@pytest.fixture(autouse=True)
def no_potc_plugins():
    with mock_potc_plugins(clear=True):
        yield
