import os
from unittest import mock

import pytest

from igm.env import env


@pytest.mark.unittest
class TestTemplateEnv:
    @mock.patch.dict(os.environ, {"ENV_ONE": "mytemp", 'ENV2': "yes"}, clear=True)
    def test_env(self):
        assert env['ENV_ONE'] == 'mytemp'
        assert env['ENV2'] == 'yes'
        assert env['NOT_FOUND'] is None

        assert env.ENV_ONE == 'mytemp'
        assert env.ENV2 == 'yes'
        assert env.NOT_FOUND is None

        assert len(env) == 2
        assert dict(env) == {"ENV_ONE": "mytemp", 'ENV2': "yes"}

        assert str(env).startswith('environ({') and str(env).endswith('})')
