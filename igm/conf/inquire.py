from contextlib import contextmanager
from typing import Mapping, ContextManager

from igm.env.inquire import user_inq_with


@contextmanager
def with_user_inquire(v: Mapping) -> ContextManager:
    """
    Overview:
        Hang the user inquire information up for templating.

    :param v: New user inquire information.

    Examples::
        >>> from igm.env import user
        >>> user
        UserInquire({})
        >>>
        >>> from igm.conf import with_user_inquire
        >>> with with_user_inquire({'a': 1, 'b': 'hansbug'}):
        ...     user
        ...
        UserInquire({'a': 1, 'b': 'hansbug'})
        >>>
        >>> user
        UserInquire({})
    """
    with user_inq_with(v):
        yield
