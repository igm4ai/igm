from typing import Iterable, Optional

from tqdm import tqdm

from igm.utils import tqdm_ncols


class RenderTask:
    def __init__(self, jobs: Iterable['RenderJob']):
        self.__jobs = list(jobs)

    def __len__(self):
        return len(self.__jobs)

    def _task_data(self):
        raise NotImplementedError  # pragma: no cover

    def run(self, silent: bool = False):
        # initialize
        if not silent:
            jobs = tqdm(self.__jobs, ncols=tqdm_ncols())
            pgbar = jobs
        else:
            jobs = self.__jobs
            pgbar = None

        # run jobs
        for job in jobs:
            job.run(self._task_data(), pgbar, silent=silent)

        # run complete
        if pgbar:
            pgbar.set_description('Complete.')
            pgbar.update()


class RenderJob:
    def __init__(self, srcpath, dstpath=None):
        self.srcpath = srcpath
        self.dstpath = dstpath

    def run(self, task_data, pgbar: Optional[tqdm], silent: bool = False):
        raise NotImplementedError  # pragma: no cover
