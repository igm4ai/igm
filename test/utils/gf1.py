from igm.utils import get_global

TT = get_global('value', default=233, stacklevel=0)
TTX = get_global('value', default=233, stacklevel=1)


def method(ft):
    return get_global('value', default=2) ** ft


TF = method(3)


def method1(ft):
    def inner_method():
        return get_global('value', default=2) ** ft

    return inner_method()


TF1 = method1(3)


def method2(ft):
    def inner_method():
        def inner_method2():
            return get_global('value', default=2) ** ft

        return inner_method2()

    return inner_method()


TF2 = method2(3)

FIXED = 2754
