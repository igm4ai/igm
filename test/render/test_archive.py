import os.path

import pytest
from hbutils.testing import isolated_directory

from igm.render.archive import ArchiveUnpackJob
from test.testings import get_testfile_path


@pytest.mark.unittest
class TestRenderArchive:
    @pytest.mark.parametrize(
        ['fmt', 'ext'],
        [
            ('7z', '.7z'),
            ('rar', '.rar'),
            ('bztar', '.tar.bz2'),
            ('gztar', '.tar.gz'),
            ('tar', '.tar'),
            ('xztar', '.tar.xz'),
            ('zip', '.zip'),
        ]
    )
    def test_archive_job(self, fmt, ext):
        with isolated_directory({f'archive{ext}': get_testfile_path(f'{fmt}_template-simple{ext}')}):
            archive_file = os.path.abspath(f'archive{ext}')
            with isolated_directory():
                job = ArchiveUnpackJob(archive_file, 'main')
                job.run(silent=True)

                assert os.path.exists('main')
                assert os.path.isdir('main')
                assert os.path.exists('main/README.md')
                assert os.path.exists('main/meta.py')
