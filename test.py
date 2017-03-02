'''
Created on 2017/03/01

@author: sakurai
'''
from importlib import import_module
from io import StringIO
import sys
from unittest import main
from unittest import mock
from unittest import TestCase
from unittest import TestLoader

from python_wrap_cases import wrap_case


@wrap_case
class Lib2to3ImportTest(TestCase):
    FIX = "lib2to3.fixes.fix_{}"

    def setUp(self):
        self.path_hooks = sys.path_hooks.copy()
        sys.path_importer_cache.clear()

    def tearDown(self):
        sys.path_hooks = self.path_hooks
        sys.path_importer_cache.clear()

    @wrap_case([FIX.format("print")], "py2codes.", "py2codes.py2_print")
    @wrap_case([FIX.format("exec")], "py2codes.", "py2codes.py2_exec")
    def test_lib2to3importer(self, fixers, prefix, modname):
        from lib2to3import import lib2to3importer
        from lib2to3import import prepending

        sys.modules.pop(modname, None)
        self.assertRaises(SyntaxError, import_module, modname)

        with prepending(lib2to3importer(fixers, prefix)):
            self.assertNotEqual(sys.path_hooks, self.path_hooks)
            with mock.patch("sys.stdout", new_callable=StringIO):
                import_module(modname)

        self.assertSequenceEqual(sys.path_hooks, self.path_hooks)


def suite():
    return TestLoader().loadTestsFromTestCase(Lib2to3ImportTest)


if __name__ == "__main__":
    main()
