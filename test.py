'''
Created on 2017/03/01

@author: sakurai
'''
from importlib import import_module
from io import StringIO
from subprocess import check_output
import sys
from unittest import main
from unittest import mock
from unittest import skipIf
from unittest import TestCase
from unittest import TestLoader

from python_wrap_cases import wrap_case


def is_installed(package):
    pip_freeze = [sys.executable, "-m", "pip", "freeze"]
    for line in check_output(pip_freeze, universal_newlines=True).splitlines():
        if line.startswith(package):
            return True
    else:
        return False


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

    def test_lib2to3importer__ctypes(self):
        from lib2to3import import lib2to3importer
        from lib2to3import import prepending

        with prepending(lib2to3importer([], "foo.bar")):
            import _ctypes
            assert _ctypes

    @skipIf(not is_installed("pysandbox"), "pysandbox is not installed")
    def test_lib2to3importer_pysandbox(self):
        from lib2to3import import lib2to3importer
        from lib2to3import import prepending

        fixers = [
            "lib2to3.fixes.fix_exec",
            "lib2to3.fixes.fix_long",
            "lib2to3.fixes.fix_unicode",
            "lib2to3.fixes.fix_imports",
            "lib2to3.fixes.fix_dict",
        ]
        with prepending(lib2to3importer(fixers, "sandbox")):
            from sandbox import Sandbox
            from sandbox import SandboxConfig
            from sandbox import SandboxError
        box = Sandbox(SandboxConfig(use_subprocess=True))
        self.assertRaises(SandboxError, box.call, print, "123")


def suite():
    return TestLoader().loadTestsFromTestCase(Lib2to3ImportTest)


if __name__ == "__main__":
    main()
