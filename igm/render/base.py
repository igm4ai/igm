import sys
from functools import partial
from typing import Iterable


class RenderTask:
    def __init__(self, jobs: Iterable['RenderJob']):
        self.__jobs = list(jobs)

    def __len__(self):
        return len(self.__jobs)

    def run(self, stream=None):
        stream = stream or sys.stdout
        for job in self.__jobs:
            job.run(stream)


class RenderJob:
    def __init__(self, srcpath, dstpath=None):
        self.srcpath = srcpath
        self.dstpath = dstpath

    def run(self, stream=None):
        stream = stream or sys.stdout
        self._run(partial(print, file=stream))

    def _run(self, log):
        raise NotImplementedError  # pragma: no cover
