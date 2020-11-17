
import os

# https://stackoverflow.com/a/59969843
try:
    # pip >=20
    from pip._internal.req import parse_requirements
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.req import parse_requirements
    except ImportError:
        # pip <= 9.0.3
        from pip.req import parse_requirements
from setuptools import setup

import lib2to3import


def from_here(*paths):
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, *paths)


classifiers = """\
License :: OSI Approved :: MIT License
Development Status :: 3 - Alpha
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Intended Audience :: Developers
""".splitlines()

keywords = """\
2to3
lib2to3
import
importer
""".splitlines()

description = lib2to3import.__doc__.splitlines()[3]

requirements_txt = parse_requirements(from_here("requirements.txt"),
                                      session="")
# https://stackoverflow.com/a/62127548
try:
    install_requires = [str(ir.req) for ir in requirements_txt]
except AttributeError:
    install_requires = [str(ir.requirement) for ir in requirements_txt]

with open(from_here("README.rst"), "w") as fp:
    for line in lib2to3import.__doc__.splitlines():
        print(line, file=fp)

setup(
    version=lib2to3import.__version__,
    name=lib2to3import.__name__,
    license=lib2to3import.__license__,
    url="https://github.com/sakurai-youhei/lib2to3import",
    description=description,
    long_description=lib2to3import.__doc__,
    classifiers=classifiers,
    keywords=keywords,
    author=lib2to3import.__author__,
    author_email=lib2to3import.__email__,
    py_modules=[lib2to3import.__name__],
    install_requires=install_requires,
    test_suite="test.suite",
)
