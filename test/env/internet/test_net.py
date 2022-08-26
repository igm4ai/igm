import os
from unittest import skipUnless

import pytest

from igm.env.internet import internet


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestEnvInternetNet:
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    @skipUnless(not os.getenv('NO_GFW'), 'gfw required')
    def test_internet_actual_has_internet_in_gfw(self):
        assert internet
        assert internet.has_internet
        assert internet.has_gfw
        assert repr(internet) == '<Internet ok, gfw: yes>'

        assert internet.baidu
        assert internet.gitee
        assert internet.github
        assert not internet.google

        assert internet.baidu
        assert internet.baidu.ok
        assert 0.0 <= internet.baidu.ttl <= 1.0
        assert internet.baidu.address == 'baidu.com'
        assert internet.baidu.port == 80
        assert repr(internet.baidu).startswith('<BaiduConnect baidu.com:80, success, ttl:') and \
               repr(internet.baidu).endswith('ms>')

        assert not internet.google
        assert not internet.google.ok
        assert internet.google.ttl is None
        assert internet.google.address == 'google.com'
        assert internet.google.port == 80
        assert repr(internet.google) == '<GoogleConnect google.com:80, fail>'

        assert not internet('twitter.com')
        assert not internet('twitter.com')
        assert internet('twitter.com').ttl is None
        assert internet('twitter.com').address == 'twitter.com'
        assert internet('twitter.com').port == 80
        assert repr(internet('twitter.com')) == '<ConnectStatus twitter.com:80, fail>'

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    @skipUnless(not os.getenv('NO_INTERNET'), 'internet required')
    @skipUnless(os.getenv('NO_GFW'), 'no gfw required')
    def test_internet_actual_has_internet_out_of_gfw(self):
        assert internet
        assert internet.has_internet
        assert not internet.has_gfw
        assert repr(internet) == '<Internet ok, gfw: no>'

        assert internet.baidu
        assert internet.gitee
        assert internet.github
        assert internet.google

        assert internet.baidu
        assert internet.baidu.ok
        assert 0.0 <= internet.baidu.ttl <= 1.0
        assert internet.baidu.address == 'baidu.com'
        assert internet.baidu.port == 80
        assert repr(internet.baidu).startswith('<BaiduConnect baidu.com:80, success, ttl:') and \
               repr(internet.baidu).endswith('ms>')

        assert internet.google
        assert internet.google.ok
        assert 0.0 <= internet.google.ttl <= 1.0
        assert internet.google.address == 'google.com'
        assert internet.google.port == 80
        assert repr(internet.google).startswith('<GoogleConnect google.com:80, success, ttl:') and \
               repr(internet.google).endswith('ms>')

    @skipUnless(os.getenv('NO_INTERNET'), 'no internet required')
    def test_internet_actual_no_network(self):
        assert not internet
        assert not internet.has_internet
        assert repr(internet) == '<Internet unavailable>'

    def test_internet_has_internet_in_gfw(self, network_in_gfw):
        assert internet
        assert internet.has_internet
        assert internet.has_gfw
        assert repr(internet) == '<Internet ok, gfw: yes>'

        assert internet.baidu
        assert internet.gitee
        assert internet.github
        assert not internet.google

        assert internet.baidu
        assert internet.baidu.ok
        assert 0.0 <= internet.baidu.ttl <= 1.0
        assert internet.baidu.address == 'baidu.com'
        assert internet.baidu.port == 80
        assert repr(internet.baidu).startswith('<BaiduConnect baidu.com:80, success, ttl:') and \
               repr(internet.baidu).endswith('ms>')

        assert not internet.google
        assert not internet.google.ok
        assert internet.google.ttl is None
        assert internet.google.address == 'google.com'
        assert internet.google.port == 80
        assert repr(internet.google) == '<GoogleConnect google.com:80, fail>'

        assert not internet('twitter.com')
        assert not internet('twitter.com')
        assert internet('twitter.com').ttl is None
        assert internet('twitter.com').address == 'twitter.com'
        assert internet('twitter.com').port == 80
        assert repr(internet('twitter.com')) == '<ConnectStatus twitter.com:80, fail>'

    def test_internet_has_internet_out_of_gfw(self, network_out_of_gfw):
        assert internet
        assert internet.has_internet
        assert not internet.has_gfw
        assert repr(internet) == '<Internet ok, gfw: no>'

        assert internet.baidu
        assert internet.gitee
        assert internet.github
        assert internet.google

        assert internet.baidu
        assert internet.baidu.ok
        assert 0.0 <= internet.baidu.ttl <= 1.0
        assert internet.baidu.address == 'baidu.com'
        assert internet.baidu.port == 80
        assert repr(internet.baidu).startswith('<BaiduConnect baidu.com:80, success, ttl:') and \
               repr(internet.baidu).endswith('ms>')

        assert internet.google
        assert internet.google.ok
        assert 0.0 <= internet.google.ttl <= 1.0
        assert internet.google.address == 'google.com'
        assert internet.google.port == 80
        assert repr(internet.google).startswith('<GoogleConnect google.com:80, success, ttl:') and \
               repr(internet.google).endswith('ms>')

    def test_internet_on_network(self, no_network):
        assert not internet
        assert not internet.has_internet
        assert repr(internet) == '<Internet unavailable>'
