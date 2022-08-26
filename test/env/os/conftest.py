from unittest.mock import patch, MagicMock

import pytest


@pytest.fixture()
def linux_machine_1():
    with patch('platform.system', MagicMock(return_value='Linux')), \
            patch('platform.version', MagicMock(return_value='#49~20.04.1-Ubuntu SMP Thu Aug 4 19:15:44 UTC 2022')), \
            patch('platform.release', MagicMock(return_value='5.15.0-46-generic')), \
            patch('platform.node', MagicMock(return_value='hansbug-MS-7C94')):
        yield


@pytest.fixture()
def windows_machine_1():
    with patch('platform.system', MagicMock(return_value='Windows')), \
            patch('platform.version', MagicMock(return_value='10.0.19041')), \
            patch('platform.release', MagicMock(return_value='10')), \
            patch('platform.node', MagicMock(return_value='LAPTOP-37QSG5BO')):
        yield
