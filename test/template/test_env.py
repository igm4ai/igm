import os
from unittest import mock

import pytest

from igm.template import Env


@pytest.mark.unittest
class TestTemplateEnv:
    @mock.patch.dict(os.environ, {"ENV_ONE": "mytemp", 'ENV2': "yes"}, clear=True)
    def test_env_getitem(self):
        env = Env()
        assert env['ENV_ONE'] == 'mytemp'
        assert env['ENV2'] == 'yes'
        assert env['NOT_FOUND'] is None

    @mock.patch.dict(os.environ, {"ENV_ONE": "mytemp", 'ENV2': "yes"}, clear=True)
    def test_env_getattr(self):
        env = Env()
        assert env.ENV_ONE == 'mytemp'
        assert env.ENV2 == 'yes'
        assert env.NOT_FOUND is None
