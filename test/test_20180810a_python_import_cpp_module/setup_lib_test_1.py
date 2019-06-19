#!/usr/bin/env python3
#
# This code is for compiling "lib_test_1.cpp".
# Run this code as
#   python setup_lib_test_1.py build_ext --inplace
# or
#   python setup_lib_test_1.py build_ext --inplace --compiler=g++
#
# See -- https://docs.python.org/3/extending/building.html
#
# To switch compiler, we can
#   os.environ["CC"] = "g++-4.7"
#   os.environ["CXX"] = "g++-4.7"
#
import os
from distutils.core import setup, Extension
from distutils.sysconfig import get_config_var

from Cython.Distutils import build_ext


def get_ext_filename_without_platform_suffix(filename):
    name, ext = os.path.splitext(filename)
    ext_suffix = get_config_var('EXT_SUFFIX')

    if ext_suffix == ext:
        return filename

    ext_suffix = ext_suffix.replace(ext, '')
    idx = name.find(ext_suffix)

    if idx == -1:
        return filename
    else:
        return name[:idx] + ext


class BuildExtWithoutPlatformSuffix(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        return get_ext_filename_without_platform_suffix(filename)


name1 = 'lib_test_1'

module1 = Extension(name1,
                    define_macros=[('MAJOR_VERSION', '0'),
                                   ('MINOR_VERSION', '1'),
                                   ],
                    include_dirs=['/opt/local/Library/Frameworks/Python.framework/Versions/3.6/include', '/opt/local/include', '/usr/include'],
                    library_dirs=['/opt/local/Library/Frameworks/Python.framework/Versions/3.6/lib', '/opt/local/lib', '/usr/lib'],
                    libraries=['stdc++','python3.6'],
                    extra_compile_args=['-std=c++11'],
                    extra_link_args=[''],
                    language="c++",
                    sources=['%s.cpp' % (name1)],
                    )

setup(name='lib_test_1',
      version='0.1',
      description='This is a test package',
      author='',
      author_email='',
      url='',
      ext_modules=[module1],
      packages=['lib_test_1','lib_test_1.test'],
      cmdclass={'build_ext': BuildExtWithoutPlatformSuffix},
      )

# print(get_config_var('EXT_SUFFIX'))
