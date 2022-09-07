from igm.utils import get_globals


def method():
    g = get_globals()
    g['v'] = 233


v = 38947
method()
