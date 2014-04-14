import os
import sys

import wrds

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'wrds'
]

requires = [
    'pandas',
    'jaydebeapi',
    'matplotlib',
    'sqlparse'
]

setup(
        name='wrds-py',
        version=wrds.__version__,
        description="Python access to WRDS Data",
        long_description=open('README.RST').read(),
        author='Eric Stein',
        author_email='ericst@wharton.upenn.edu',
        url='http://www.whartonwrds.com',
        packages=packages,
        package_data = {
            '': ['*.rst'],
            },
        classifiers=(
           'Development Status :: 5 - Beta',
           'Environment :: Console',
           'Environment :: X11 Applications :: GTK',
           'Intended Audience :: End Users/Desktop',
           'Intended Audience :: Financial and Insurance Industry',
           'Intended Audience :: Education',
           'Intended Audience :: Science/Research',
        ),
)
        

