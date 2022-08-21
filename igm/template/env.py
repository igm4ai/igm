import os
from typing import Optional


class Env:
    @classmethod
    def _getitem(cls, item) -> Optional[str]:
        return os.environ.get(item, None)

    def __getitem__(self, item) -> Optional[str]:
        return self._getitem(item)

    def __getattr__(self, item) -> Optional[str]:
        return self._getitem(item)
