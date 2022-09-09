import os.path
import sys

import pytest
from hbutils.reflection import mount_pythonpath, quick_import_object

CURDIR, _ = os.path.split(os.path.abspath(__file__))

SOURCE_CODE = """
import gf1

my_val1 = gf1.FIXED
my_val2 = gf1.FIXED ** 2
"""


@pytest.mark.unittest
class TestUtilsPythonPath:
    def test_with_pythonpath(self):
        with pytest.raises(ImportError):
            # noinspection PyUnresolvedReferences
            import gf1

        with pytest.raises(ImportError):
            quick_import_object('gf1.FIXED')

        old_path = sys.path
        with mount_pythonpath(CURDIR):
            v = {}
            exec(SOURCE_CODE, v)
            assert v['my_val1'] == 2754
            assert v['my_val2'] == 2754 ** 2

            from gf1 import FIXED
            assert FIXED == 2754

            val, _, _ = quick_import_object('gf1.FIXED')
            assert val == 2754

        assert sys.path == old_path

        with mount_pythonpath(os.path.normpath(os.path.join(CURDIR, '..', 'testfile'))):
            from gf1 import FIXED
            assert FIXED == 1234567
