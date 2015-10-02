from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

__version__ = "0.3.6"

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md', 'CHANGES.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='silp',
    version=__version__,
    url='http://github.com/yjpark/silp/',
    description='Simple Individual Line Preprocessor',
    long_description=long_description,
    license='MIT License',
    author='YJ Park',
    author_email='yjpark@gmail.com',
    tests_require=['pytest'],
    install_requires=[
        'pytz',
        'blessings>=1.5.1',
        ],
    cmdclass={'test': PyTest},
    packages=['silp'],
    scripts=['bin/silp'],
    include_package_data=True,
    platforms='any',
    test_suite='silp.test.test_silp',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
