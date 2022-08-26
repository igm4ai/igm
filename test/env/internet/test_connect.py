import os
from unittest import skipUnless

import pytest

from igm.env.internet import try_connect


@pytest.mark.unittest
class TestEnvInternetConnect:
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    def test_try_connect_actual(self):
        baidu_ok, baidu_ttl = try_connect('baidu.com', 80)
        assert baidu_ok
        assert 0 < baidu_ttl < 1

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @skipUnless(not os.getenv('NO_GFW'), 'gfw required')
    def test_try_connect_google_actual_in_gfw(self):
        google_ok, google_ttl = try_connect('google.com', 80)
        assert not google_ttl
        assert google_ttl is None

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @skipUnless(os.getenv('NO_GFW'), 'no gfw required')
    def test_try_connect_google_actual_out_of_gfw(self):
        google_ok, google_ttl = try_connect('google.com', 80)
        assert google_ttl
        assert 0 < google_ttl < 1

    def test_try_connect_no_network(self, no_network):
        baidu_ok, baidu_ttl = try_connect('baidu.com', 80)
        assert not baidu_ok
        assert baidu_ttl is None

        gitee_ok, gitee_ttl = try_connect('gitee.com', 80)
        assert not gitee_ok
        assert gitee_ttl is None

        google_ok, google_ttl = try_connect('google.com', 80)
        assert not google_ttl
        assert google_ttl is None

    def test_try_connect_network_in_gfw(self, network_in_gfw):
        baidu_ok, baidu_ttl = try_connect('baidu.com', 80)
        assert baidu_ok
        assert 0 < baidu_ttl < 1

        gitee_ok, gitee_ttl = try_connect('gitee.com', 80)
        assert gitee_ok
        assert 0 < gitee_ttl < 1

        google_ok, google_ttl = try_connect('google.com', 80)
        assert not google_ttl
        assert google_ttl is None

    def test_try_connect_network_out_of_gfw(self, network_out_of_gfw):
        baidu_ok, baidu_ttl = try_connect('baidu.com', 80)
        assert baidu_ok
        assert 0 < baidu_ttl < 1

        gitee_ok, gitee_ttl = try_connect('gitee.com', 80)
        assert gitee_ok
        assert 0 < gitee_ttl < 1

        google_ok, google_ttl = try_connect('google.com', 80)
        assert google_ttl
        assert 0 < google_ttl < 1
